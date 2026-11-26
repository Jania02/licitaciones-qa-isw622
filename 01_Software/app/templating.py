from pathlib import Path

from fastapi.templating import Jinja2Templates

# Jinja2Templates escapa HTML por defecto en archivos .html (REQ-012).
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
