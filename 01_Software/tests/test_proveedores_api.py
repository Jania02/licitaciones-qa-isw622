"""Pruebas de integración de Proveedores: API, interfaz web, BD y seguridad."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.main import app
from app.models import Proveedor

P1 = "Tecnología Norte S.A."
P2 = "Servicios del Valle"


@pytest.fixture(autouse=True)
def limpiar_proveedores():
    with SessionLocal() as db:
        db.execute(delete(Proveedor))
        db.commit()
    yield


def crear(client, nombre):
    return client.post("/api/proveedores", json={"nombre": nombre})


# ---------- Alta, listado y unicidad (REQ-001) ----------

def test_crear_proveedor_valido(client_autenticado):
    respuesta = crear(client_autenticado, f"  {P1}  ")
    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == P1


def test_listar_proveedores(client_autenticado):
    crear(client_autenticado, P1)
    crear(client_autenticado, P2)
    nombres = [p["nombre"] for p in client_autenticado.get("/api/proveedores").json()]
    assert nombres == [P2, P1]  # orden alfabético


@pytest.mark.parametrize("variante", [
    "tecnología norte s.a.",
    "TECNOLOGÍA NORTE S.A.",
    "  Tecnología    Norte   S.A.  ",
])
def test_duplicado_por_mayusculas_o_espacios_se_rechaza(client_autenticado, variante):
    crear(client_autenticado, P1)
    respuesta = crear(client_autenticado, variante)
    assert respuesta.status_code == 409
    assert respuesta.json() == {"detail": "Ya existe un proveedor con ese nombre."}
    assert len(client_autenticado.get("/api/proveedores").json()) == 1


def test_bd_rechaza_duplicado_aunque_se_salte_la_validacion():
    with SessionLocal() as db:
        db.add(Proveedor(nombre=P1, nombre_normalizado=P1.casefold()))
        db.commit()
        db.add(Proveedor(nombre=P1.upper(), nombre_normalizado=P1.casefold()))
        with pytest.raises(IntegrityError):
            db.commit()


# ---------- Edición ----------

def test_editar_proveedor(client_autenticado):
    proveedor_id = crear(client_autenticado, P1).json()["id"]
    respuesta = client_autenticado.put(f"/api/proveedores/{proveedor_id}",
                                       json={"nombre": "Tecnología Norte Ltda."})
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Tecnología Norte Ltda."


def test_editar_cambiando_solo_mayusculas_de_su_propio_nombre(client_autenticado):
    proveedor_id = crear(client_autenticado, P1).json()["id"]
    respuesta = client_autenticado.put(f"/api/proveedores/{proveedor_id}",
                                       json={"nombre": P1.upper()})
    assert respuesta.status_code == 200


def test_editar_a_nombre_de_otro_proveedor_se_rechaza(client_autenticado):
    crear(client_autenticado, P1)
    proveedor_id = crear(client_autenticado, P2).json()["id"]
    respuesta = client_autenticado.put(f"/api/proveedores/{proveedor_id}",
                                       json={"nombre": "tecnología norte s.a."})
    assert respuesta.status_code == 409


def test_editar_inexistente_responde_404(client_autenticado):
    respuesta = client_autenticado.put("/api/proveedores/9999", json={"nombre": P1})
    assert respuesta.status_code == 404


# ---------- Eliminación ----------

def test_eliminar_proveedor(client_autenticado):
    proveedor_id = crear(client_autenticado, P1).json()["id"]
    assert client_autenticado.delete(f"/api/proveedores/{proveedor_id}").status_code == 204
    assert client_autenticado.get(f"/api/proveedores/{proveedor_id}").status_code == 404


# ---------- Validación y seguridad (REQ-011, REQ-012) ----------

@pytest.mark.parametrize("nombre", ["Norte@Sur", "<script>alert(1)</script>", "   "])
def test_api_rechaza_nombres_invalidos(client_autenticado, nombre):
    respuesta = crear(client_autenticado, nombre)
    assert respuesta.status_code == 400
    assert client_autenticado.get("/api/proveedores").json() == []


@pytest.mark.parametrize("nombre", ["Norte\tSur", "Norte\nSur", "Tecnología Norte S.A.\n"])
def test_api_rechaza_tabulaciones_y_saltos_de_linea(client_autenticado, nombre):
    respuesta = crear(client_autenticado, nombre)
    assert respuesta.status_code == 400
    assert client_autenticado.get("/api/proveedores").json() == []


def test_api_sin_sesion_responde_401(client):
    assert client.get("/api/proveedores").status_code == 401
    assert crear(client, P1).status_code == 401


def test_web_muestra_script_rechazado_como_texto_escapado(client_autenticado):
    respuesta = client_autenticado.post("/proveedores",
                                        data={"nombre": "<script>alert(1)</script>"})
    assert respuesta.status_code == 400
    assert "<script>alert(1)</script>" not in respuesta.text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in respuesta.text


def test_error_interno_no_expone_detalles():
    def falla():
        raise RuntimeError("detalle secreto: ruta C:/db password=123")

    app.add_api_route("/api/_prueba_error", falla)
    respuesta = TestClient(app, raise_server_exceptions=False).get("/api/_prueba_error")
    assert respuesta.status_code == 500
    assert respuesta.json() == {"detail": "Ocurrió un error interno. Intente de nuevo."}
    assert "secreto" not in respuesta.text


# ---------- Interfaz web ----------

def test_web_crear_y_listar(client_autenticado):
    respuesta = client_autenticado.post("/proveedores", data={"nombre": P1},
                                        follow_redirects=False)
    assert respuesta.status_code == 303
    assert P1 in client_autenticado.get("/proveedores").text


def test_web_duplicado_muestra_mensaje(client_autenticado):
    client_autenticado.post("/proveedores", data={"nombre": P1})
    respuesta = client_autenticado.post("/proveedores", data={"nombre": P1.lower()})
    assert respuesta.status_code == 400
    assert "Ya existe un proveedor con ese nombre." in respuesta.text


def test_web_editar(client_autenticado):
    proveedor_id = crear(client_autenticado, P1).json()["id"]
    client_autenticado.post(f"/proveedores/{proveedor_id}/editar", data={"nombre": P2})
    assert P2 in client_autenticado.get("/proveedores").text


def test_web_sin_sesion_redirige_a_login(client):
    respuesta = client.get("/proveedores", follow_redirects=False)
    assert respuesta.headers["location"] == "/login"
