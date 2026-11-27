"""REQ-007/008/009: evaluación y rangos configurables en céntimos CRC."""
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import Integer, String, select, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, Session
from app.auth import usuario_actual
from app.database import Base, get_db, SessionLocal
from app.licitaciones import centimos, crc, obtener
from app.ofertas import Oferta
from app.templating import templates

router = APIRouter(dependencies=[Depends(usuario_actual)])

class Rango(Base):
    __tablename__ = 'rangos_aprobacion'
    __table_args__ = (CheckConstraint('minimo > 0'), CheckConstraint('maximo IS NULL OR maximo >= minimo'))
    id: Mapped[int] = mapped_column(primary_key=True)
    minimo: Mapped[int] = mapped_column(Integer)
    maximo = mapped_column(Integer, nullable=True)
    aprobador: Mapped[str] = mapped_column(String(100))

class Entrada(BaseModel):
    minimo_crc: Decimal
    maximo_crc: Decimal | None = None
    aprobador: str

def inicializar_rangos():
    with SessionLocal() as db:
        if db.scalar(select(Rango.id).limit(1)) is None:
            db.add_all([Rango(minimo=1,maximo=99999999,aprobador='Encargado de área'), Rango(minimo=100000000,maximo=999999999,aprobador='Gerencia'), Rango(minimo=1000000000,maximo=None,aprobador='Junta Directiva')])
            db.commit()

def ahorro(presupuesto, monto):
    porcentaje = Decimal(presupuesto-monto)*100/Decimal(presupuesto)
    return porcentaje, 'conveniente' if porcentaje >= 10 else 'aceptable' if porcentaje > 0 else 'válida sin ahorro'

def mejor_oferta(ofertas):
    return min(ofertas, key=lambda o:(o.monto_centimos,o.registrada_en,o.id), default=None)

def aprobador(rangos, monto):
    return next((r.aprobador for r in rangos if r.minimo <= monto and (r.maximo is None or monto <= r.maximo)), None)

def rangos(db):
    return list(db.scalars(select(Rango).order_by(Rango.minimo)))

def datos_rango(db, datos, excluir=None):
    minimo=centimos(datos.minimo_crc)
    maximo=centimos(datos.maximo_crc) if datos.maximo_crc is not None else None
    nombre=datos.aprobador.strip()
    if not nombre or len(nombre)>100 or (maximo is not None and maximo < minimo):
        raise HTTPException(400,'Rango inválido.')
    for r in rangos(db):
        if r.id != excluir and (maximo is None or r.minimo <= maximo) and (r.maximo is None or minimo <= r.maximo):
            raise HTTPException(409,'Los rangos no pueden traslaparse.')
    return dict(minimo=minimo,maximo=maximo,aprobador=nombre)

def salida(r):
    return dict(id=r.id,minimo_crc=crc(r.minimo),maximo_crc=crc(r.maximo) if r.maximo is not None else None,aprobador=r.aprobador)

def buscar(db,id):
    r=db.get(Rango,id)
    if r is None: raise HTTPException(404,'Rango no encontrado.')
    return r

@router.get('/api/rangos')
def listar(db:Session=Depends(get_db)):
    return [salida(r) for r in rangos(db)]

@router.post('/api/rangos',status_code=201)
def crear(datos:Entrada,db:Session=Depends(get_db)):
    r=Rango(**datos_rango(db,datos)); db.add(r); db.commit(); db.refresh(r); return salida(r)

@router.put('/api/rangos/{id}')
def editar(id:int,datos:Entrada,db:Session=Depends(get_db)):
    r=buscar(db,id)
    for k,v in datos_rango(db,datos,id).items(): setattr(r,k,v)
    db.commit(); return salida(r)

@router.delete('/api/rangos/{id}',status_code=204)
def eliminar(id:int,db:Session=Depends(get_db)):
    db.delete(buscar(db,id)); db.commit(); return Response(status_code=204)

@router.get('/api/evaluacion/{id}')
def evaluar(id:int,db:Session=Depends(get_db)):
    l=obtener(db,id)
    o=mejor_oferta(db.scalars(select(Oferta).where(Oferta.licitacion_id==id,Oferta.monto_centimos>0,Oferta.monto_centimos<=l.presupuesto_centimos,Oferta.registrada_en<l.cierre)))
    if o is None: return {'mensaje':'Sin ofertas válidas','mejor_oferta':None}
    porcentaje,clasificacion=ahorro(l.presupuesto_centimos,o.monto_centimos)
    return dict(mejor_oferta=crc(o.monto_centimos),proveedor_id=o.proveedor_id,ahorro_porcentaje=str(porcentaje.quantize(Decimal('0.01'))),clasificacion=clasificacion,aprobador=aprobador(rangos(db),o.monto_centimos))

@router.get('/evaluacion')
def pagina(request:Request,usuario=Depends(usuario_actual)):
    return templates.TemplateResponse(request,'evaluacion.html',{'usuario':usuario})
