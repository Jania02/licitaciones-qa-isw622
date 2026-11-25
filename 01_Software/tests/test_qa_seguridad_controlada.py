import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.parametrize('nombre',['Norte@Sur','<script>alert(1)</script>'])
def test_nombre_rechazado_en_api(client_autenticado,nombre):
    c=client_autenticado; antes=c.get('/api/proveedores').json()
    r=c.post('/api/proveedores',json={'nombre':nombre})
    assert r.status_code==400
    assert c.get('/api/proveedores').json()==antes
    assert '<script>' not in r.text


def test_error_validacion_no_refleja_entrada(client_autenticado):
    r=client_autenticado.post('/api/licitaciones',json={'codigo':'QA','titulo':'Prueba','presupuesto_crc':'VALOR-SINTETICO','cierre':'incorrecto'})
    assert r.status_code==422
    assert r.json()=={'detail':'Datos de entrada inválidos.'}
    assert 'VALOR-SINTETICO' not in r.text


def test_api_sin_sesion(client):
    assert client.get('/api/licitaciones').status_code==401
    assert client.post('/api/ofertas',json={'licitacion_id':1,'proveedor_id':1,'monto_crc':'1'}).status_code==401
