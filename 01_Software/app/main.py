from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database import Base, engine

app = FastAPI(title="Sistema de Gestión de Licitaciones")

Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    return "<h1>Sistema de Gestión de Licitaciones</h1>"
