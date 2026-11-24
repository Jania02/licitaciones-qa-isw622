from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(200))


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Nombre tal como se muestra (sin espacios sobrantes).
    nombre: Mapped[str] = mapped_column(String(100))
    # Clave de unicidad: espacios compactados y sin distinguir mayúsculas (REQ-001).
    # La restricción UNIQUE hace que la base de datos también rechace duplicados.
    nombre_normalizado: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora_utc)
