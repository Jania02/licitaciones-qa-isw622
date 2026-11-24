# Sistema de Gestión de Licitaciones — Práctica Integradora QA (ISW-622, UTN)

Aplicación web local con FastAPI + SQLite, pruebas con pytest y Postman.
La división del trabajo está en [docs/PLAN_EQUIPO.md](docs/PLAN_EQUIPO.md).

## Estructura

| Carpeta | Contenido |
|---|---|
| `01_Software/` | Código fuente, pruebas, seed y scripts |
| `02_Plan_Informe_QA/` | Plantilla Word completada y su PDF |
| `03_Registro_QA/` | Plantilla Excel completada |
| `04_Evidencias/` | Salidas reales, capturas, logs y reportes (nombre con ID EV-###) |
| `05_IA/` | Prompts y salidas saneadas (IA-###) |
| `docs/` | Plan del equipo y notas |

## Requisitos

- Python 3.11+

## Instalación y ejecución

```powershell
cd 01_Software
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

- Interfaz: http://127.0.0.1:8000
- Swagger (API): http://127.0.0.1:8000/docs

## Pruebas

```powershell
cd 01_Software
pytest -v
```

## Base de datos

SQLite en `01_Software/licitaciones.db` (ruta configurable en `.env`).
Reinicio y carga de datos sintéticos: _pendiente (issue de seed)_.

## Usuarios de prueba

Al arrancar, la app crea el usuario definido en `.env` (`ADMIN_USER` / `ADMIN_PASSWORD`) si no existe.
Con el `.env.example` por defecto: usuario `admin`, contraseña `admin123` (solo datos sintéticos).

Las contraseñas se guardan con hash PBKDF2-SHA256. Todas las pantallas y la API (salvo `/login`,
`/api/auth/login` y `/api/health`) requieren sesión iniciada:

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/login` | JSON `{"username", "password"}` → 200 o 401 |
| POST | `/api/auth/logout` | Cierra la sesión |
| GET | `/api/auth/me` | Usuario actual o 401 |

## Flujo de trabajo Git

1. Tomar un issue y crear una rama: `git checkout -b feat/<tema>`.
2. Commits pequeños y descriptivos.
3. Abrir Pull Request hacia `main` con `Closes #<issue>`; otro integrante lo revisa y aprueba.
4. Nunca hacer push directo a `main`.
