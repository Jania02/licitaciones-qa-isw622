"""BUG-001: oferta exactamente en el instante de cierre (REQ-004).

CP-010 es el caso que detecta el defecto; el resto son pruebas de regresión
sobre plazo y estado (REQ-004) y montos (REQ-005).
"""

from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from sqlalchemy import delete

import app.ofertas as ofertas
from app.database import SessionLocal
from app.licitaciones import Licitacion, ahora
from app.models import Proveedor

CIERRE = ahora() + timedelta(days=1)
UN_INSTANTE = timedelta(microseconds=1)


def licitacion(estado="Publicada"):
    return SimpleNamespace(estado=estado, cierre=CIERRE, presupuesto_centimos=10000)


@pytest.fixture
def datos_oferta(client_autenticado):
    """Licitación publicada y proveedor propios de la prueba."""
    with SessionLocal() as db:
        nueva = Licitacion(codigo="LIC-BUG-001", titulo="Cierre exacto",
                           presupuesto_centimos=10000, cierre=CIERRE, estado="Publicada")
        proveedor = Proveedor(nombre="Proveedor Bug", nombre_normalizado="proveedor bug")
        db.add_all([nueva, proveedor])
        db.commit()
        ids = {"licitacion_id": nueva.id, "proveedor_id": proveedor.id}
    yield {**ids, "monto_crc": "100"}
    with SessionLocal() as db:
        db.execute(delete(ofertas.Oferta).where(
            ofertas.Oferta.licitacion_id == ids["licitacion_id"]))
        db.execute(delete(Licitacion).where(Licitacion.id == ids["licitacion_id"]))
        db.execute(delete(Proveedor).where(Proveedor.id == ids["proveedor_id"]))
        db.commit()


# ---------- CP-010: exactamente al cierre ----------

def test_cp010_unitaria_exactamente_al_cierre_se_rechaza():
    with pytest.raises(HTTPException) as error:
        ofertas.validar_oferta(licitacion(), Decimal("100"), CIERRE)
    assert error.value.status_code == 400


def test_cp010_api_exactamente_al_cierre_se_rechaza(client_autenticado, datos_oferta, monkeypatch):
    monkeypatch.setattr(ofertas, "ahora", lambda: CIERRE)
    respuesta = client_autenticado.post("/api/ofertas", json=datos_oferta)
    assert respuesta.status_code == 400
    consulta = f"/api/ofertas?licitacion_id={datos_oferta['licitacion_id']}"
    assert client_autenticado.get(consulta).json() == []


# ---------- Regresión ----------

def test_regresion_antes_del_cierre_se_acepta():
    assert ofertas.validar_oferta(licitacion(), Decimal("100"), CIERRE - UN_INSTANTE) == 10000


def test_regresion_despues_del_cierre_se_rechaza():
    with pytest.raises(HTTPException):
        ofertas.validar_oferta(licitacion(), Decimal("100"), CIERRE + UN_INSTANTE)


@pytest.mark.parametrize("estado", ["Borrador", "Cerrada"])
def test_regresion_estado_no_publicado_se_rechaza(estado):
    with pytest.raises(HTTPException):
        ofertas.validar_oferta(licitacion(estado), Decimal("100"), CIERRE - UN_INSTANTE)


@pytest.mark.parametrize("monto", ["0", "-1", "100.01"])
def test_regresion_monto_invalido_se_rechaza(monto):
    with pytest.raises(HTTPException):
        ofertas.validar_oferta(licitacion(), Decimal(monto), CIERRE - UN_INSTANTE)


def test_regresion_api_antes_del_cierre_crea_la_oferta(client_autenticado, datos_oferta, monkeypatch):
    monkeypatch.setattr(ofertas, "ahora", lambda: CIERRE - UN_INSTANTE)
    assert client_autenticado.post("/api/ofertas", json=datos_oferta).status_code == 201
