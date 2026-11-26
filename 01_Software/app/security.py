"""Hash y verificación de contraseñas con PBKDF2-SHA256 (biblioteca estándar)."""

import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 260_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), ITERACIONES
    ).hex()
    return f"{ALGORITMO}${ITERACIONES}${salt}${digest}"


def verify_password(password: str, almacenado: str) -> bool:
    try:
        algoritmo, iteraciones, salt, digest = almacenado.split("$")
        if algoritmo != ALGORITMO:
            return False
        calculado = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iteraciones)
        ).hex()
    except (ValueError, AttributeError):
        return False
    return hmac.compare_digest(calculado, digest)
