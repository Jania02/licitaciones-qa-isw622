"""Pruebas unitarias del hash de contraseñas."""

from app.security import hash_password, verify_password


def test_hash_no_guarda_la_contrasena_en_texto_plano():
    almacenado = hash_password("secreta123")
    assert "secreta123" not in almacenado
    assert almacenado.startswith("pbkdf2_sha256$")


def test_verificar_contrasena_correcta():
    assert verify_password("secreta123", hash_password("secreta123")) is True


def test_verificar_contrasena_incorrecta():
    assert verify_password("otra", hash_password("secreta123")) is False


def test_misma_contrasena_genera_hashes_distintos():
    assert hash_password("secreta123") != hash_password("secreta123")


def test_hash_malformado_no_valida():
    assert verify_password("secreta123", "texto-invalido") is False
