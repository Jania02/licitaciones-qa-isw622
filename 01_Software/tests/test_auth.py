"""Pruebas de integración de autenticación (interfaz web y API)."""

from tests.conftest import CREDENCIALES


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
    assert "Bienvenido, admin" in inicio.text


def test_login_web_contrasena_incorrecta_muestra_error(client):
    respuesta = client.post("/login", data={"username": "admin", "password": "mala"})
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
    assert respuesta.json() == {"usuario": "admin"}


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
    assert respuesta.json() == {"usuario": "admin"}


def test_logout_api_invalida_la_sesion(client_autenticado):
    client_autenticado.post("/api/auth/logout")
    assert client_autenticado.get("/api/auth/me").status_code == 401
