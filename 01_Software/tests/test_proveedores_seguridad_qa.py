"""Pruebas complementarias de Proveedores y seguridad (REQ-001, REQ-011, REQ-012).

El resultado esperado de cada prueba sale de los requisitos del enunciado.
"""

import pytest
from sqlalchemy import delete

from app.database import SessionLocal
from app.models import Proveedor
from app.proveedores_service import ErrorValidacion, clave_unicidad, validar_nombre

P1 = "Tecnología Norte S.A."
P2 = "Servicios del Valle"
CONTROL = ["Norte\tSur", "Norte\nSur"]
MOTIVO_CONTROL = "Pendiente en PR #32: tabulaciones y saltos de línea se compactan en vez de rechazarse."


@pytest.fixture(autouse=True)
def limpiar_proveedores():
    def limpiar():
        with SessionLocal() as db:
            db.execute(delete(Proveedor))
            db.commit()

    limpiar()
    yield
    limpiar()


def nombres(client):
    return [p["nombre"] for p in client.get("/api/proveedores").json()]


# ---------- Unitarias ----------

@pytest.mark.parametrize("variante", [
    "tecnología norte s.a.",
    "TECNOLOGÍA NORTE S.A.",
    " Tecnología  Norte  S.A. ",
])
def test_variantes_de_p1_comparten_clave(variante):
    assert clave_unicidad(variante) == clave_unicidad(P1)


def test_nombres_distintos_no_comparten_clave():
    assert clave_unicidad(P1) != clave_unicidad(P2)


@pytest.mark.parametrize("simbolo", list("_/\\!?:;\"'*+=%$[]{}|"))
def test_simbolo_no_admitido_se_rechaza(simbolo):
    with pytest.raises(ErrorValidacion):
        validar_nombre(f"Norte{simbolo}Sur")


@pytest.mark.xfail(strict=True, reason=MOTIVO_CONTROL)
@pytest.mark.parametrize("nombre", CONTROL)
def test_caracter_de_control_se_rechaza(nombre):
    with pytest.raises(ErrorValidacion):
        validar_nombre(nombre)


# ---------- Integración API e interfaz ----------

def test_duplicado_en_interfaz_de_un_alta_por_api(client_autenticado):
    c = client_autenticado
    assert c.post("/api/proveedores", json={"nombre": P1}).status_code == 201
    respuesta = c.post("/proveedores", data={"nombre": f"  {P1.upper()}  "})
    assert respuesta.status_code == 400
    assert nombres(c) == [P1]


@pytest.mark.parametrize("nombre", ["Norte@Sur", "<img src=x onerror=alert(1)>"])
def test_api_e_interfaz_rechazan_lo_mismo(client_autenticado, nombre):
    c = client_autenticado
    assert c.post("/api/proveedores", json={"nombre": nombre}).status_code == 400
    web = c.post("/proveedores", data={"nombre": nombre})
    assert web.status_code == 400
    assert "<img src=x" not in web.text
    assert nombres(c) == []


@pytest.mark.parametrize("nombre", ["Norte@Sur", "<script>alert(1)</script>"])
def test_edicion_invalida_conserva_el_nombre(client_autenticado, nombre):
    c = client_autenticado
    proveedor_id = c.post("/api/proveedores", json={"nombre": P1}).json()["id"]
    respuesta = c.put(f"/api/proveedores/{proveedor_id}", json={"nombre": nombre})
    assert respuesta.status_code == 400
    assert nombres(c) == [P1]


@pytest.mark.xfail(strict=True, reason=MOTIVO_CONTROL)
@pytest.mark.parametrize("nombre", CONTROL)
def test_api_rechaza_caracter_de_control(client_autenticado, nombre):
    respuesta = client_autenticado.post("/api/proveedores", json={"nombre": nombre})
    assert respuesta.status_code == 400
