from datetime import datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace as S
import pytest
from fastapi import HTTPException
from app.evaluacion import mejor_oferta, ahorro, aprobador
from app.moneda import convertir, validar_tasa

@pytest.mark.parametrize('monto,pct,clase',[(90000000,10,'conveniente'),(95000000,5,'aceptable'),(100000000,0,'válida sin ahorro')])
def test_ahorro(monto,pct,clase):
    assert ahorro(100000000,monto)==(Decimal(pct),clase)

def test_mejor_y_empate():
    t=datetime(2026,1,1);a=S(id=1,monto_centimos=100,registrada_en=t);b=S(id=2,monto_centimos=100,registrada_en=t+timedelta(seconds=1));c=S(id=3,monto_centimos=200,registrada_en=t)
    assert mejor_oferta([c,b,a]) is a
    assert mejor_oferta([]) is None

@pytest.mark.parametrize('monto,nombre',[(1,'Área'),(99999999,'Área'),(100000000,'Gerencia'),(999999999,'Gerencia'),(1000000000,'Junta')])
def test_aprobadores(monto,nombre):
    rangos=[S(minimo=1,maximo=99999999,aprobador='Área'),S(minimo=100000000,maximo=999999999,aprobador='Gerencia'),S(minimo=1000000000,maximo=None,aprobador='Junta')]
    assert aprobador(rangos,monto)==nombre

def test_conversion():
    assert convertir('9000000','500')==Decimal('18000.00')
    with pytest.raises(HTTPException): validar_tasa(Decimal('0'))

def test_moneda_no_cambia_importes(client_autenticado):
    c=client_autenticado
    r=c.post('/api/tasas',json={'crc_por_usd':'500'});assert r.status_code==201,r.text
    try:
        antes=c.get('/api/licitaciones').json()
        assert c.get('/api/moneda?moneda=USD').status_code==200
        assert c.get('/api/licitaciones').json()==antes
    finally: c.delete('/api/tasas/'+str(r.json()['id']))
