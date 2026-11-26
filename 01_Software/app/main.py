import os
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import models  # noqa: F401  (registra las tablas)
from app.auth import LoginRequerido, usuario_actual
from app.auth import router as auth_router
from app.database import Base, engine
from app.models import Usuario
from app.templating import templates

BASE_DIR = Path(__file__).parent

# La clave que firma las cookies de sesión es obligatoria y solo vive en .env.
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise RuntimeError("Falta SECRET_KEY en el archivo .env (ver .env.example).")

app = FastAPI(title="Sistema de Gestión de Licitaciones")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    same_site="lax",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

Base.metadata.create_all(bind=engine)


@app.exception_handler(LoginRequerido)
def manejar_login_requerido(request: Request, exc: LoginRequerido):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": "Debe iniciar sesión."}, status_code=401)
    return RedirectResponse("/login", status_code=303)


app.include_router(auth_router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index(request: Request, usuario: Usuario = Depends(usuario_actual)):
    return templates.TemplateResponse(request, "index.html", {"usuario": usuario})
