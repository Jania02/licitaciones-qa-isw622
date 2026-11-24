"""Pruebas unitarias de las reglas de Proveedores (REQ-001, REQ-012). No usan la BD."""

import pytest

from app.proveedores_service import (
    MSG_CARACTERES,
    MSG_LARGO,
    MSG_VACIO,
    ErrorValidacion,
    clave_unicidad,
    normalizar_nombre,
    validar_nombre,
)


def test_normalizar_recorta_y_compacta_espacios():
    assert normalizar_nombre("   Tecnología    Norte   S.A.  ") == "Tecnología Norte S.A."


def test_clave_ignora_mayusculas_y_espacios():
    assert clave_unicidad("tecnología norte s.a.") == clave_unicidad("  TECNOLOGÍA   Norte S.A. ")


@pytest.mark.parametrize("nombre", [
    "Tecnología Norte S.A.",
    "Servicios del Valle",
    "Ferretería Pérez, Hijos (Sede 2)",
    "Ñandú 123",
])
def test_nombres_validos(nombre):
    assert validar_nombre(nombre) == nombre


@pytest.mark.parametrize("nombre", ["", "    ", None])
def test_nombre_vacio_se_rechaza(nombre):
    with pytest.raises(ErrorValidacion) as error:
        validar_nombre(nombre)
    assert error.value.mensaje == MSG_VACIO


@pytest.mark.parametrize("nombre", [
    "Norte@Sur",
    "Proveedor #1",
    "A&B",
    "Comercial-Norte",
    "<script>alert(1)</script>",
    "<b>Negrita</b>",
    "Nombre'; DROP TABLE proveedores;--",
])
def test_caracteres_no_permitidos_se_rechazan(nombre):
    with pytest.raises(ErrorValidacion) as error:
        validar_nombre(nombre)
    assert error.value.mensaje == MSG_CARACTERES


def test_longitud_limite():
    assert validar_nombre("A" * 100) == "A" * 100
    with pytest.raises(ErrorValidacion) as error:
        validar_nombre("A" * 101)
    assert error.value.mensaje == MSG_LARGO
