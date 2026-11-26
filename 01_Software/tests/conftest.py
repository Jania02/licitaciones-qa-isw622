import os
import secrets
import tempfile
from pathlib import Path

# Entorno SOLO de prueba, generado al azar en cada ejecución: no hay credenciales
# escritas en el código. Se define antes de importar la app.
_tmp = Path(tempfile.mkdtemp())
os.environ["DATABASE_URL"] = f"sqlite:///{(_tmp / 'test.db').as_posix()}"
os.environ["SECRET_KEY"] = secrets.token_hex(32)
os.environ["ADMIN_USER"] = "usuario_prueba"
os.environ["ADMIN_PASSWORD"] = secrets.token_urlsafe(16)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.auth import crear_admin_inicial  # noqa: E402
from app.main import app  # noqa: E402

# El usuario de prueba se crea igual que con seed.py.
crear_admin_inicial()

USUARIO = os.environ["ADMIN_USER"]
CREDENCIALES = {"username": USUARIO, "password": os.environ["ADMIN_PASSWORD"]}


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def client_autenticado(client):
    respuesta = client.post("/api/auth/login", json=CREDENCIALES)
    assert respuesta.status_code == 200
    return client
