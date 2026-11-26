"""Pruebas de integración de autenticación (interfaz web y API)."""

import os
from pathlib import Path

from app.auth import crear_admin_inicial

from tests.conftest import CREDENCIALES, USUARIO


# ---------- Interfaz web ----------

def test_inicio_sin_sesion_redirige_a_login(client):
    respuesta = client.get("/", follow_redirects=False)
    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/login"


def test_login_web_correcto_entra_al_inicio(client):
    respuesta = client.post("/login", data=CREDENCIALES, follow_redirects=False)
    assert respuesta.status_code == 303
    assert respuesta.headers["location"] == "/"

    inicio = client.get("/")
    assert inicio.status_code == 200
    assert f"Bienvenido, {USUARIO}" in inicio.text


def test_login_web_contrasena_incorrecta_muestra_error(client):
    respuesta = client.post("/login", data={"username": USUARIO, "password": "mala"})
    assert respuesta.status_code == 401
    assert "Usuario o contraseña incorrectos." in respuesta.text


def test_logout_web_cierra_la_sesion(client):
    client.post("/login", data=CREDENCIALES)
    client.post("/logout")
    respuesta = client.get("/", follow_redirects=False)
    assert respuesta.headers["location"] == "/login"


# ---------- API ----------

def test_login_api_correcto(client):
    respuesta = client.post("/api/auth/login", json=CREDENCIALES)
    assert respuesta.status_code == 200
    assert respuesta.json() == {"usuario": USUARIO}


def test_login_api_usuario_inexistente(client):
    respuesta = client.post("/api/auth/login", json={"username": "nadie", "password": "x"})
    assert respuesta.status_code == 401
    assert respuesta.json() == {"detail": "Usuario o contraseña incorrectos."}


def test_api_protegida_sin_sesion_responde_401(client):
    respuesta = client.get("/api/auth/me")
    assert respuesta.status_code == 401


def test_api_me_con_sesion(client_autenticado):
    respuesta = client_autenticado.get("/api/auth/me")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"usuario": USUARIO}


def test_logout_api_invalida_la_sesion(client_autenticado):
    client_autenticado.post("/api/auth/logout")
    assert client_autenticado.get("/api/auth/me").status_code == 401


# ---------- Configuración ----------

def test_seed_crea_el_usuario_de_prueba_desde_el_entorno():
    # Ejecutarlo de nuevo no duplica el usuario y confirma que lee .env.
    assert crear_admin_inicial() is True


def test_seed_sin_contrasena_no_crea_usuario(monkeypatch):
    monkeypatch.setenv("ADMIN_PASSWORD", "")
    assert crear_admin_inicial() is False


def test_app_exige_secret_key(tmp_path):
    import subprocess, sys
    # Vacía a propósito: python-dotenv no reemplaza una variable ya definida,
    # así que tampoco la toma de un .env local.
    env = {**os.environ, "SECRET_KEY": ""}
    env["DATABASE_URL"] = f"sqlite:///{(tmp_path / 'x.db').as_posix()}"
    resultado = subprocess.run(
        [sys.executable, "-c", "import app.main"],
        cwd=Path(__file__).resolve().parents[1], env=env, capture_output=True, text=True,
    )
    assert resultado.returncode != 0
    assert "Falta SECRET_KEY" in resultado.stderr
