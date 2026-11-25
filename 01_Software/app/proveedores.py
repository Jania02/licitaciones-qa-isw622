"""Rutas de Proveedores: interfaz web y API HTTP. Todas requieren sesión."""

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import proveedores_service as servicio
from app.auth import usuario_actual
from app.database import get_db
from app.models import Proveedor, Usuario
from app.templating import templates

router = APIRouter()


class ProveedorEntrada(BaseModel):
    nombre: str


def a_dict(proveedor: Proveedor) -> dict:
    return {"id": proveedor.id, "nombre": proveedor.nombre}


def error_json(exc: Exception) -> JSONResponse:
    if isinstance(exc, servicio.ProveedorNoEncontrado):
        return JSONResponse({"detail": str(exc)}, status_code=404)
    if isinstance(exc, servicio.ProveedorDuplicado):
        return JSONResponse({"detail": exc.mensaje}, status_code=409)
    return JSONResponse({"detail": exc.mensaje}, status_code=400)


ERRORES = (servicio.ErrorValidacion, servicio.ProveedorNoEncontrado)


# ---------- API ----------

@router.get("/api/proveedores")
def api_listar(db: Session = Depends(get_db), _: Usuario = Depends(usuario_actual)):
    return [a_dict(p) for p in servicio.listar(db)]


@router.get("/api/proveedores/{proveedor_id}")
def api_obtener(proveedor_id: int, db: Session = Depends(get_db),
                _: Usuario = Depends(usuario_actual)):
    try:
        return a_dict(servicio.obtener(db, proveedor_id))
    except ERRORES as exc:
        return error_json(exc)


@router.post("/api/proveedores", status_code=201)
def api_crear(datos: ProveedorEntrada, db: Session = Depends(get_db),
              _: Usuario = Depends(usuario_actual)):
    try:
        return a_dict(servicio.crear(db, datos.nombre))
    except ERRORES as exc:
        return error_json(exc)


@router.put("/api/proveedores/{proveedor_id}")
def api_editar(proveedor_id: int, datos: ProveedorEntrada, db: Session = Depends(get_db),
               _: Usuario = Depends(usuario_actual)):
    try:
        return a_dict(servicio.editar(db, proveedor_id, datos.nombre))
    except ERRORES as exc:
        return error_json(exc)


@router.delete("/api/proveedores/{proveedor_id}", status_code=204)
def api_eliminar(proveedor_id: int, db: Session = Depends(get_db),
                 _: Usuario = Depends(usuario_actual)):
    try:
        servicio.eliminar(db, proveedor_id)
    except ERRORES as exc:
        return error_json(exc)
    return Response(status_code=204)


# ---------- Interfaz web ----------

def _pagina_lista(request, db, usuario, error=None, nombre="", status_code=200):
    return templates.TemplateResponse(
        request,
        "proveedores/lista.html",
        {"usuario": usuario, "proveedores": servicio.listar(db),
         "error": error, "nombre": nombre},
        status_code=status_code,
    )


@router.get("/proveedores")
def web_listar(request: Request, db: Session = Depends(get_db),
               usuario: Usuario = Depends(usuario_actual)):
    return _pagina_lista(request, db, usuario)


@router.post("/proveedores")
def web_crear(request: Request, nombre: str = Form(""), db: Session = Depends(get_db),
              usuario: Usuario = Depends(usuario_actual)):
    try:
        servicio.crear(db, nombre)
    except servicio.ErrorValidacion as exc:
        return _pagina_lista(request, db, usuario, exc.mensaje, nombre, status_code=400)
    return RedirectResponse("/proveedores", status_code=303)


@router.get("/proveedores/{proveedor_id}/editar")
def web_editar_form(proveedor_id: int, request: Request, db: Session = Depends(get_db),
                    usuario: Usuario = Depends(usuario_actual)):
    try:
        proveedor = servicio.obtener(db, proveedor_id)
    except servicio.ProveedorNoEncontrado:
        return RedirectResponse("/proveedores", status_code=303)
    return templates.TemplateResponse(
        request, "proveedores/editar.html",
        {"usuario": usuario, "proveedor": proveedor, "nombre": proveedor.nombre, "error": None},
    )


@router.post("/proveedores/{proveedor_id}/editar")
def web_editar(proveedor_id: int, request: Request, nombre: str = Form(""),
               db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_actual)):
    try:
        servicio.editar(db, proveedor_id, nombre)
    except servicio.ProveedorNoEncontrado:
        return RedirectResponse("/proveedores", status_code=303)
    except servicio.ErrorValidacion as exc:
        proveedor = servicio.obtener(db, proveedor_id)
        return templates.TemplateResponse(
            request, "proveedores/editar.html",
            {"usuario": usuario, "proveedor": proveedor, "nombre": nombre, "error": exc.mensaje},
            status_code=400,
        )
    return RedirectResponse("/proveedores", status_code=303)


@router.post("/proveedores/{proveedor_id}/eliminar")
def web_eliminar(proveedor_id: int, db: Session = Depends(get_db),
                 _: Usuario = Depends(usuario_actual)):
    try:
        servicio.eliminar(db, proveedor_id)
    except servicio.ProveedorNoEncontrado:
        pass
    except servicio.ProveedorDuplicado as exc:
        return JSONResponse({"detail": exc.mensaje}, status_code=409)
    return RedirectResponse("/proveedores", status_code=303)
