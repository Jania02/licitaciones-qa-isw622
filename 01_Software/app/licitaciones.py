"""REQ-002 y REQ-003. Los importes se almacenan en céntimos CRC."""
from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import String, Integer, DateTime, CheckConstraint, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column, Session
from app.database import Base, get_db
from app.auth import usuario_actual
from app.templating import templates

router = APIRouter(dependencies=[Depends(usuario_actual)])
ESTADOS = {"Borrador": {"Publicada", "Cerrada"}, "Publicada": {"Cerrada"}, "Cerrada": set()}

def ahora():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def utc(fecha):
    if fecha.tzinfo is None:
        raise HTTPException(400, "Indique una fecha con zona horaria.")
    return fecha.astimezone(timezone.utc).replace(tzinfo=None)

def centimos(monto: Decimal):
    if not monto.is_finite() or not 0 < monto <= Decimal("999999999999.99") or monto * 100 != (monto * 100).to_integral_value():
        raise HTTPException(400, "Monto positivo con máximo dos decimales requerido.")
    return int(monto * 100)

def crc(valor):
    return format(Decimal(valor) / 100, ".2f")

class Licitacion(Base):
    __tablename__ = "licitaciones"
    __table_args__ = (CheckConstraint("presupuesto_centimos > 0"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(60), unique=True)
    titulo: Mapped[str] = mapped_column(String(200))
    presupuesto_centimos: Mapped[int] = mapped_column(Integer)
    cierre: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(String(12), default="Borrador")

class Entrada(BaseModel):
    codigo: str
    titulo: str
    presupuesto_crc: Decimal
    cierre: datetime

class Estado(BaseModel):
    estado: str

def validar(datos, instante=None):
    codigo, titulo = datos.codigo.strip().upper(), datos.titulo.strip()
    cierre = utc(datos.cierre)
    if not codigo or len(codigo) > 60 or not titulo or len(titulo) > 200:
        raise HTTPException(400, "Código y título son obligatorios (máximo 60 y 200 caracteres).")
    if cierre <= (instante if instante is not None else ahora()):
        raise HTTPException(400, "El cierre debe ser futuro.")
    return dict(codigo=codigo, titulo=titulo, presupuesto_centimos=centimos(datos.presupuesto_crc), cierre=cierre)

def validar_transicion(actual, destino, cierre, instante):
    if destino not in ESTADOS[actual]:
        raise HTTPException(400, "Transición de estado no permitida.")
    if destino == "Publicada" and cierre <= instante:
        raise HTTPException(400, "No se puede publicar una licitación vencida.")

def obtener(db, id):
    obj = db.get(Licitacion, id)
    if obj is None:
        raise HTTPException(404, "Licitación no encontrada.")
    return obj

def guardar(db, obj):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Código de licitación duplicado.")
    db.refresh(obj)
    return obj

def salida(obj):
    return dict(id=obj.id, codigo=obj.codigo, titulo=obj.titulo, presupuesto_crc=crc(obj.presupuesto_centimos),
                cierre=obj.cierre.replace(tzinfo=timezone.utc).isoformat(), estado=obj.estado)

@router.get("/api/licitaciones")
def listar(db: Session = Depends(get_db)):
    return [salida(x) for x in db.scalars(select(Licitacion).order_by(Licitacion.id))]

@router.get("/api/licitaciones/{id}")
def detalle(id: int, db: Session = Depends(get_db)):
    return salida(obtener(db, id))

@router.post("/api/licitaciones", status_code=201)
def crear(datos: Entrada, db: Session = Depends(get_db)):
    obj = Licitacion(**validar(datos))
    db.add(obj)
    return salida(guardar(db, obj))

@router.put("/api/licitaciones/{id}")
def editar(id: int, datos: Entrada, db: Session = Depends(get_db)):
    obj = obtener(db, id)
    if obj.estado != "Borrador":
        raise HTTPException(409, "Solo se permite editar borradores.")
    for k, v in validar(datos).items():
        setattr(obj, k, v)
    return salida(guardar(db, obj))

@router.patch("/api/licitaciones/{id}/estado")
def cambiar_estado(id: int, datos: Estado, db: Session = Depends(get_db)):
    obj = obtener(db, id)
    validar_transicion(obj.estado, datos.estado, obj.cierre, ahora())
    obj.estado = datos.estado
    return salida(guardar(db, obj))

@router.delete("/api/licitaciones/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    obj = obtener(db, id)
    if obj.estado != "Borrador":
        raise HTTPException(409, "Solo se permite eliminar borradores.")
    db.delete(obj)
    db.commit()
    return Response(status_code=204)

@router.get("/licitaciones")
def pagina(request: Request, usuario=Depends(usuario_actual)):
    return templates.TemplateResponse(request, "licitaciones.html", {"usuario": usuario})
