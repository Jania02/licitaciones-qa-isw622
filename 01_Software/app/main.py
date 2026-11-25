import logging
import os
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import models  # noqa: F401  (registra las tablas)
from app.auth import LoginRequerido, crear_admin_inicial, usuario_actual
from app.auth import router as auth_router
from app.database import Base, engine
from app.models import Usuario
from app.proveedores import router as proveedores_router
from app.templating import templates
from app.ofertas import router as ofertas_router
from app.licitaciones import router as licitaciones_router

BASE_DIR = Path(__file__).parent
logger = logging.getLogger("licitaciones")

app = FastAPI(title="Sistema de Gestión de Licitaciones")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "solo-desarrollo-local"),
    same_site="lax",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

Base.metadata.create_all(bind=engine)
crear_admin_inicial()


@app.exception_handler(LoginRequerido)
def manejar_login_requerido(request: Request, exc: LoginRequerido):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": "Debe iniciar sesión."}, status_code=401)
    return RedirectResponse("/login", status_code=303)


@app.exception_handler(Exception)
def manejar_error_interno(request: Request, exc: Exception):
    # REQ-012: el detalle queda solo en el log del servidor, nunca en la respuesta.
    logger.exception("Error no controlado en %s", request.url.path)
    return JSONResponse(
        {"detail": "Ocurrió un error interno. Intente de nuevo."}, status_code=500
    )


app.include_router(auth_router)
app.include_router(proveedores_router)
app.include_router(ofertas_router)
app.include_router(licitaciones_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index(request: Request, usuario: Usuario = Depends(usuario_actual)):
    return templates.TemplateResponse(request, "index.html", {"usuario": usuario})
