"""Autenticación con usuario y contraseña (sesión por cookie firmada)."""

import os

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models import Usuario
from app.security import hash_password, verify_password
from app.templating import templates

router = APIRouter()

MENSAJE_LOGIN_INVALIDO = "Usuario o contraseña incorrectos."


class LoginRequerido(Exception):
    """Se lanza cuando una ruta protegida se usa sin sesión iniciada."""


class Credenciales(BaseModel):
    username: str
    password: str


def autenticar(db: Session, username: str, password: str) -> Usuario | None:
    usuario = db.scalar(select(Usuario).where(Usuario.username == username.strip()))
    if usuario is None or not verify_password(password, usuario.password_hash):
        return None
    return usuario


def usuario_actual(request: Request, db: Session = Depends(get_db)) -> Usuario:
    usuario_id = request.session.get("usuario_id")
    usuario = db.get(Usuario, usuario_id) if usuario_id else None
    if usuario is None:
        raise LoginRequerido()
    return usuario


def crear_admin_inicial() -> None:
    """Crea el usuario de prueba definido en .env si todavía no existe."""
    username = os.getenv("ADMIN_USER", "").strip()
    password = os.getenv("ADMIN_PASSWORD", "")
    if not username or not password:
        return
    with SessionLocal() as db:
        existe = db.scalar(select(Usuario).where(Usuario.username == username))
        if existe is None:
            db.add(Usuario(username=username, password_hash=hash_password(password)))
            db.commit()


# ---------- Interfaz web ----------

@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
def login_web(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    db: Session = Depends(get_db),
):
    usuario = autenticar(db, username, password)
    if usuario is None:
        return templates.TemplateResponse(
            request, "login.html", {"error": MENSAJE_LOGIN_INVALIDO}, status_code=401
        )
    request.session.clear()
    request.session["usuario_id"] = usuario.id
    return RedirectResponse("/", status_code=303)


@router.post("/logout")
def logout_web(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


# ---------- API ----------

@router.post("/api/auth/login")
def login_api(datos: Credenciales, request: Request, db: Session = Depends(get_db)):
    usuario = autenticar(db, datos.username, datos.password)
    if usuario is None:
        return JSONResponse({"detail": MENSAJE_LOGIN_INVALIDO}, status_code=401)
    request.session.clear()
    request.session["usuario_id"] = usuario.id
    return {"usuario": usuario.username}


@router.post("/api/auth/logout")
def logout_api(request: Request):
    request.session.clear()
    return {"detail": "Sesión cerrada."}


@router.get("/api/auth/me")
def me(usuario: Usuario = Depends(usuario_actual)):
    return {"usuario": usuario.username}
