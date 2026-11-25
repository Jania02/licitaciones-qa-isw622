"""REQ-004/005/006. Una oferta por licitación y proveedor."""
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, Session
from app.auth import usuario_actual
from app.database import Base, get_db
from app.models import Proveedor
from app.licitaciones import ahora, centimos, crc, obtener, Licitacion
from app.templating import templates

router = APIRouter(dependencies=[Depends(usuario_actual)])

class Oferta(Base):
    __tablename__ = "ofertas"
    __table_args__ = (UniqueConstraint("licitacion_id", "proveedor_id"), CheckConstraint("monto_centimos > 0"))
    id: Mapped[int] = mapped_column(primary_key=True)
    licitacion_id: Mapped[int] = mapped_column(ForeignKey("licitaciones.id", ondelete="RESTRICT"))
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id", ondelete="RESTRICT"))
    monto_centimos: Mapped[int] = mapped_column(Integer)
    registrada_en: Mapped[datetime] = mapped_column(DateTime, default=ahora)

class Entrada(BaseModel):
    licitacion_id: int
    proveedor_id: int
    monto_crc: Decimal

class CambioMonto(BaseModel):
    monto_crc: Decimal

def validar_oferta(licitacion, monto, instante):
    if licitacion.estado != "Publicada" or instante > licitacion.cierre:
        raise HTTPException(400, "La licitación no admite ofertas en este momento.")
    valor = centimos(monto)
    if valor > licitacion.presupuesto_centimos:
        raise HTTPException(400, "La oferta supera el presupuesto.")
    return valor

def salida(o):
    return dict(id=o.id, licitacion_id=o.licitacion_id, proveedor_id=o.proveedor_id, monto_crc=crc(o.monto_centimos), registrada_en=o.registrada_en.replace(tzinfo=timezone.utc).isoformat())

def buscar(db, id):
    o = db.get(Oferta, id)
    if o is None:
        raise HTTPException(404, "Oferta no encontrada.")
    return o

@router.get("/api/ofertas")
def listar(licitacion_id: int | None = None, proveedor_id: int | None = None, db: Session = Depends(get_db)):
    q = select(Oferta)
    if licitacion_id is not None:
        q = q.where(Oferta.licitacion_id == licitacion_id)
    if proveedor_id is not None:
        q = q.where(Oferta.proveedor_id == proveedor_id)
    return [salida(o) for o in db.scalars(q.order_by(Oferta.id))]

@router.get("/api/ofertas/{id}")
def detalle(id: int, db: Session = Depends(get_db)):
    return salida(buscar(db, id))

@router.post("/api/ofertas", status_code=201)
def crear(datos: Entrada, db: Session = Depends(get_db)):
    l = obtener(db, datos.licitacion_id)
    if db.get(Proveedor, datos.proveedor_id) is None:
        raise HTTPException(404, "Proveedor no encontrado.")
    instante = ahora()
    o = Oferta(licitacion_id=l.id, proveedor_id=datos.proveedor_id, monto_centimos=validar_oferta(l, datos.monto_crc, instante), registrada_en=instante)
    db.add(o)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Oferta duplicada o referencia no disponible.")
    db.refresh(o)
    return salida(o)

@router.put("/api/ofertas/{id}")
def editar(id: int, datos: CambioMonto, db: Session = Depends(get_db)):
    o = buscar(db, id)
    instante = ahora()
    o.monto_centimos = validar_oferta(obtener(db, o.licitacion_id), datos.monto_crc, instante)
    # La modificación es una nueva presentación a efectos de desempate.
    o.registrada_en = instante
    db.commit()
    return salida(o)

@router.delete("/api/ofertas/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    o = buscar(db, id)
    validar_oferta(obtener(db, o.licitacion_id), Decimal(o.monto_centimos)/100, ahora())
    db.delete(o)
    db.commit()
    return Response(status_code=204)

@router.get("/ofertas")
def pagina(request: Request, usuario=Depends(usuario_actual)):
    return templates.TemplateResponse(request, "ofertas.html", {"usuario": usuario})
