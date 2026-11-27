"""Reglas de negocio de Proveedores (REQ-001 y REQ-012).

Este módulo no depende de FastAPI: lo usan tanto la interfaz web como la API,
así ambas aplican exactamente las mismas validaciones (REQ-011).
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Proveedor

LONGITUD_MAXIMA = 100
CARACTERES_PERMITIDOS_EXTRA = set(" .,()")

MSG_VACIO = "El nombre del proveedor es obligatorio."
MSG_LARGO = f"El nombre no puede superar {LONGITUD_MAXIMA} caracteres."
MSG_CARACTERES = (
    "El nombre solo puede contener letras, números, espacios, punto, coma y paréntesis."
)
MSG_DUPLICADO = "Ya existe un proveedor con ese nombre."
MSG_NO_EXISTE = "El proveedor no existe."


class ErrorValidacion(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class ProveedorDuplicado(ErrorValidacion):
    pass


class ProveedorNoEncontrado(Exception):
    pass


# ---------- Reglas puras ----------

def normalizar_nombre(nombre: str) -> str:
    """Recorta los extremos y compacta espacios internos: '  A   B ' -> 'A B'."""
    return " ".join((nombre or "").split())


def clave_unicidad(nombre: str) -> str:
    """Clave para detectar duplicados sin distinguir mayúsculas."""
    return normalizar_nombre(nombre).casefold()


def caracter_permitido(c: str) -> bool:
    return c.isalpha() or c in "0123456789" or c in CARACTERES_PERMITIDOS_EXTRA


def tiene_espacio_no_permitido(nombre: str) -> bool:
    """Tabulaciones, saltos de línea y otros espacios o caracteres de control.

    Se revisa ANTES de normalizar, porque normalizar los convertiría en espacios
    y el nombre se aceptaría.
    """
    return any((c.isspace() and c != " ") or not c.isprintable() for c in (nombre or ""))


def validar_nombre(nombre: str) -> str:
    """Devuelve el nombre normalizado o lanza ErrorValidacion."""
    if tiene_espacio_no_permitido(nombre):
        raise ErrorValidacion(MSG_CARACTERES)
    limpio = normalizar_nombre(nombre)
    if not limpio:
        raise ErrorValidacion(MSG_VACIO)
    if len(limpio) > LONGITUD_MAXIMA:
        raise ErrorValidacion(MSG_LARGO)
    if not all(caracter_permitido(c) for c in limpio):
        raise ErrorValidacion(MSG_CARACTERES)
    return limpio


# ---------- Operaciones con la base de datos ----------

def listar(db: Session) -> list[Proveedor]:
    return list(db.scalars(select(Proveedor).order_by(Proveedor.nombre)))


def obtener(db: Session, proveedor_id: int) -> Proveedor:
    proveedor = db.get(Proveedor, proveedor_id)
    if proveedor is None:
        raise ProveedorNoEncontrado(MSG_NO_EXISTE)
    return proveedor


def _verificar_no_duplicado(db: Session, clave: str, excluir_id: int | None = None) -> None:
    consulta = select(Proveedor.id).where(Proveedor.nombre_normalizado == clave)
    if excluir_id is not None:
        consulta = consulta.where(Proveedor.id != excluir_id)
    if db.scalar(consulta) is not None:
        raise ProveedorDuplicado(MSG_DUPLICADO)


def _guardar(db: Session, proveedor: Proveedor) -> Proveedor:
    try:
        db.commit()
    except IntegrityError:
        # Respaldo de la restricción UNIQUE si dos altas llegan a la vez.
        db.rollback()
        raise ProveedorDuplicado(MSG_DUPLICADO)
    db.refresh(proveedor)
    return proveedor


def crear(db: Session, nombre: str) -> Proveedor:
    limpio = validar_nombre(nombre)
    clave = limpio.casefold()
    _verificar_no_duplicado(db, clave)
    proveedor = Proveedor(nombre=limpio, nombre_normalizado=clave)
    db.add(proveedor)
    return _guardar(db, proveedor)


def editar(db: Session, proveedor_id: int, nombre: str) -> Proveedor:
    proveedor = obtener(db, proveedor_id)
    limpio = validar_nombre(nombre)
    clave = limpio.casefold()
    _verificar_no_duplicado(db, clave, excluir_id=proveedor_id)
    proveedor.nombre = limpio
    proveedor.nombre_normalizado = clave
    return _guardar(db, proveedor)


def eliminar(db: Session, proveedor_id: int) -> None:
    proveedor = obtener(db, proveedor_id)
    db.delete(proveedor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ProveedorDuplicado("No se puede eliminar un proveedor con ofertas registradas.")
