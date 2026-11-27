from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4
import pytest
from fastapi import HTTPException
from app.licitaciones import validar_transicion, ahora
from app.ofertas import validar_oferta
from app.database import SessionLocal
from app.licitaciones import Licitacion
from sqlalchemy import select


def test_transiciones():
    t=ahora(); cierre=t+timedelta(seconds=1)
    for a,b in [('Borrador','Publicada'),('Borrador','Cerrada'),('Publicada','Cerrada')]:
        validar_transicion(a,b,cierre,t)
    for a,b in [('Publicada','Borrador'),('Cerrada','Publicada'),('Cerrada','Borrador')]:
        with pytest.raises(HTTPException): validar_transicion(a,b,cierre,t)
    with pytest.raises(HTTPException): validar_transicion('Borrador','Publicada',t,t)

@pytest.mark.parametrize('monto,valido',[('0',False),('-1',False),('100',True),('100.01',False)])
def test_montos(monto,valido):
    t=ahora(); l=SimpleNamespace(estado='Publicada',cierre=t+timedelta(seconds=1),presupuesto_centimos=10000)
    if valido: assert validar_oferta(l,Decimal(monto),t)==10000
    else:
        with pytest.raises(HTTPException): validar_oferta(l,Decimal(monto),t)

@pytest.mark.parametrize('estado,segundos,valido',[('Publicada',-1,True),('Publicada',0,False),('Publicada',1,False),('Borrador',-1,False),('Cerrada',-1,False)])
def test_vencimiento(estado,segundos,valido):
    t=ahora(); l=SimpleNamespace(estado=estado,cierre=t,presupuesto_centimos=10000)
    if valido: assert validar_oferta(l,Decimal('1'),t+timedelta(seconds=segundos))==100
    else:
        with pytest.raises(HTTPException): validar_oferta(l,Decimal('1'),t+timedelta(seconds=segundos))


def crear_licitacion(client):
    codigo='QA-'+uuid4().hex
    r=client.post('/api/licitaciones',json=dict(codigo=codigo,titulo='Prueba QA',presupuesto_crc='100',cierre=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()))
    assert r.status_code==201,r.text
    return r.json()['id'],codigo


def test_api_licitacion_duplicada(client_autenticado):
    c=client_autenticado; id,codigo=crear_licitacion(c)
    r=c.post('/api/licitaciones',json=dict(codigo=' '+codigo.lower()+' ',titulo='Duplicado',presupuesto_crc='100',cierre=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()))
    assert r.status_code==409,r.text
    assert c.get(f'/api/licitaciones/{id}').status_code==200


def test_api_ofertas(client_autenticado):
    c=client_autenticado; l,_=crear_licitacion(c)
    p=c.post('/api/proveedores',json={'nombre':'Proveedor '+uuid4().hex});assert p.status_code==201,p.text
    p=p.json()['id']; datos=dict(licitacion_id=l,proveedor_id=p,monto_crc='100')
    try:
        assert c.post('/api/ofertas',json=datos).status_code==400
        assert c.patch(f'/api/licitaciones/{l}/estado',json={'estado':'Publicada'}).status_code==200
        r=c.post('/api/ofertas',json=datos);assert r.status_code==201,r.text
        assert c.post('/api/ofertas',json=datos).status_code==409
        assert len(c.get(f'/api/ofertas?licitacion_id={l}&proveedor_id={p}').json())==1
        with SessionLocal() as db:
            db.get(Licitacion,l).cierre=ahora()-timedelta(seconds=1);db.commit()
        assert c.post('/api/ofertas',json=datos).status_code==400
    finally:
        # Limpiar referencias para no interferir con la suite de proveedores.
        from app.ofertas import Oferta
        from sqlalchemy import delete
        with SessionLocal() as db:
            db.execute(delete(Oferta).where(Oferta.licitacion_id==l));db.execute(delete(Licitacion).where(Licitacion.id==l));db.commit()
        c.delete(f'/api/proveedores/{p}')
