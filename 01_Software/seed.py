"""Inicialización de la base de datos y datos sintéticos para QA."""

import argparse
import os
from datetime import timedelta

from app import models, licitaciones, ofertas, evaluacion, moneda
from app.auth import crear_admin_inicial
from app.database import Base, engine, SessionLocal
from app.proveedores_service import crear


def validar_credenciales():
    if not os.getenv("ADMIN_USER", "").strip() or not os.getenv("ADMIN_PASSWORD"):
        raise SystemExit(
            "Defina ADMIN_USER y ADMIN_PASSWORD en .env."
        )


def inicializar():
    validar_credenciales()
    Base.metadata.create_all(bind=engine)

    if not crear_admin_inicial():
        raise SystemExit("No se pudo crear el usuario de prueba.")

    evaluacion.inicializar_rangos()


def seed():
    if engine.url.get_backend_name() != "sqlite":
        raise SystemExit("Solo SQLite local está permitido.")

    validar_credenciales()

    Base.metadata.drop_all(engine)
    inicializar()

    with SessionLocal() as db:
        p1 = crear(db, "Tecnología Norte S.A.")
        p2 = crear(db, "Servicios del Valle")

        cierre = licitaciones.ahora() + timedelta(hours=48)

        l = licitaciones.Licitacion(
            codigo="LIC-2026-001",
            titulo="Equipo tecnológico",
            presupuesto_centimos=1000000000,
            cierre=cierre,
            estado="Publicada",
        )

        db.add(l)
        db.flush()

        db.add_all([
            ofertas.Oferta(
                licitacion_id=l.id,
                proveedor_id=p1.id,
                monto_centimos=900000000,
            ),
            ofertas.Oferta(
                licitacion_id=l.id,
                proveedor_id=p2.id,
                monto_centimos=950000000,
            ),
        ])

        for i, monto in enumerate(
            [90000000, 95000000, 100000000], start=1
        ):
            l = licitaciones.Licitacion(
                codigo=f"LIC-LIM-{i}",
                titulo=f"Escenario aislado {i}",
                presupuesto_centimos=100000000,
                cierre=cierre,
                estado="Publicada",
            )

            db.add(l)
            db.flush()

            db.add(
                ofertas.Oferta(
                    licitacion_id=l.id,
                    proveedor_id=p1.id,
                    monto_centimos=monto,
                )
            )

        db.add(moneda.Tasa(crc_por_usd="500", fuente="manual"))
        db.commit()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Borra todos los datos de la BD SQLite configurada.",
    )

    args = parser.parse_args()

    if args.reset:
        seed()
        print("Datos sintéticos cargados.")
    else:
        inicializar()
        print("Tablas listas y usuario de prueba preparado.")


if __name__ == "__main__":
    main()