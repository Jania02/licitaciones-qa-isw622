import os
import tempfile
from pathlib import Path

# Base de datos y credenciales SOLO de prueba; se definen antes de importar la app.
_tmp = Path(tempfile.mkdtemp())
os.environ["DATABASE_URL"] = f"sqlite:///{(_tmp / 'test.db').as_posix()}"
os.environ["SECRET_KEY"] = "clave-solo-para-pruebas"
os.environ["ADMIN_USER"] = "admin"
os.environ["ADMIN_PASSWORD"] = "admin123"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

CREDENCIALES = {"username": "admin", "password": "admin123"}


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def client_autenticado(client):
    respuesta = client.post("/api/auth/login", json=CREDENCIALES)
    assert respuesta.status_code == 200
    return client
