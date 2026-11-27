"""REQ-010: tasa CRC/USD persistida; conversión solo en lectura."""
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone
import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import String, DateTime, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from app.auth import usuario_actual
from app.database import Base, get_db
from app.licitaciones import ahora, Licitacion, crc
from app.ofertas import Oferta
from app.templating import templates

router=APIRouter(dependencies=[Depends(usuario_actual)])
class Tasa(Base):
    __tablename__='tipos_cambio'
    id:Mapped[int]=mapped_column(primary_key=True)
    crc_por_usd:Mapped[str]=mapped_column(String(50))
    registrada_en:Mapped[datetime]=mapped_column(DateTime,default=ahora)
    fuente:Mapped[str]=mapped_column(String(50),default='manual')
class Entrada(BaseModel):
    crc_por_usd:Decimal

def validar_tasa(tasa):
    if not tasa.is_finite() or not Decimal('0.000001') <= tasa <= Decimal('1000000000'):
        raise HTTPException(400,'La tasa debe ser positiva y estar dentro del rango admitido.')
    return format(tasa,'f')

def convertir(monto_crc,tasa):
    return (Decimal(monto_crc)/Decimal(validar_tasa(Decimal(tasa)))).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)

def salida(t):
    return dict(id=t.id,crc_por_usd=t.crc_por_usd,fecha=t.registrada_en.replace(tzinfo=timezone.utc).isoformat(),fuente=t.fuente)

def guardar(db,tasa,fuente='manual'):
    t=Tasa(crc_por_usd=validar_tasa(tasa),fuente=fuente);db.add(t);db.commit();db.refresh(t);return salida(t)

def buscar(db,id):
    t=db.get(Tasa,id)
    if t is None: raise HTTPException(404,'Tasa no encontrada.')
    return t

@router.get('/api/tasas')
def listar(db:Session=Depends(get_db)):
    return [salida(t) for t in db.scalars(select(Tasa).order_by(Tasa.registrada_en.desc(),Tasa.id.desc()))]
@router.post('/api/tasas',status_code=201)
def crear(datos:Entrada,db:Session=Depends(get_db)):
    return guardar(db,datos.crc_por_usd)
@router.put('/api/tasas/{id}')
def editar(id:int,datos:Entrada,db:Session=Depends(get_db)):
    t=buscar(db,id);t.crc_por_usd=validar_tasa(datos.crc_por_usd);t.registrada_en=ahora();t.fuente='manual';db.commit();return salida(t)
@router.delete('/api/tasas/{id}',status_code=204)
def eliminar(id:int,db:Session=Depends(get_db)):
    db.delete(buscar(db,id));db.commit();return Response(status_code=204)
@router.post('/api/tasas/externa',status_code=201)
def externa(db:Session=Depends(get_db)):
    try:
        r=httpx.get('https://open.er-api.com/v6/latest/USD',timeout=5);r.raise_for_status()
        tasa=Decimal(str(r.json()['rates']['CRC']));validar_tasa(tasa)
    except (httpx.HTTPError,KeyError,ValueError,ArithmeticError,HTTPException):
        raise HTTPException(503,'Servicio externo no disponible. Puede registrar una tasa manual.')
    return guardar(db,tasa,'open.er-api.com')
@router.get('/api/moneda')
def vista(moneda:str='CRC',db:Session=Depends(get_db)):
    if moneda not in ('CRC','USD'): raise HTTPException(400,'Moneda inválida.')
    t=db.scalar(select(Tasa).order_by(Tasa.registrada_en.desc(),Tasa.id.desc()).limit(1))
    if moneda=='USD' and t is None: raise HTTPException(409,'Configure una tasa primero.')
    def mostrar(c): return crc(c) if moneda=='CRC' else str(convertir(crc(c),t.crc_por_usd))
    return dict(moneda=moneda,tasa=salida(t) if t else None,licitaciones=[dict(codigo=l.codigo,presupuesto=mostrar(l.presupuesto_centimos)) for l in db.scalars(select(Licitacion))],ofertas=[dict(id=o.id,monto=mostrar(o.monto_centimos)) for o in db.scalars(select(Oferta))])
@router.get('/moneda')
def pagina(request:Request,usuario=Depends(usuario_actual)):
    return templates.TemplateResponse(request,'moneda.html',{'usuario':usuario})
