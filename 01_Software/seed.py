"""Prepara la base de datos local: crea las tablas y el usuario de prueba.

Uso (desde 01_Software, con el .env configurado):
    python seed.py

El usuario y la contraseña se leen de ADMIN_USER y ADMIN_PASSWORD en .env;
no hay credenciales escritas en el código.
"""
from app import models  # noqa: F401  (registra las tablas)
from app.auth import crear_admin_inicial
from app.database import Base, engine


def main() -> None:
    Base.metadata.create_all(bind=engine)
    if not crear_admin_inicial():
        raise SystemExit("Defina ADMIN_USER y ADMIN_PASSWORD en .env y vuelva a ejecutar.")
    print("Tablas listas y usuario de prueba creado (o ya existía).")


if __name__ == "__main__":
    main()
