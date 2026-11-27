"""Respuesta de validación uniforme sin eco de datos sensibles (REQ-011/012)."""
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def registrar_errores(app):
    @app.exception_handler(RequestValidationError)
    async def error_validacion(request, exc):
        return JSONResponse({"detail": "Datos de entrada inválidos."}, status_code=422)
