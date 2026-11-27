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
copy .env.example .env      # luego completar SECRET_KEY y ADMIN_PASSWORD en .env
python seed.py              # crea las tablas y el usuario de prueba
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
Reinicio y carga de datos sintéticos (detener el servidor antes): desde `01_Software`, ejecutar `python seed.py --reset`. **Borra los datos de la BD SQLite configurada**. Usar únicamente con datos de laboratorio. Incluye P1/P2, L1, ofertas, tasa 500, rangos y tres escenarios de frontera. El usuario de prueba se crea con las variables de `.env`.

## Usuarios de prueba

No hay credenciales en el código ni en el repositorio. En `.env` (que no se sube) se definen:

- `SECRET_KEY`: obligatoria; la app no arranca sin ella. Generarla con
  `python -c "import secrets; print(secrets.token_hex(32))"`.
- `ADMIN_USER` y `ADMIN_PASSWORD`: usuario de prueba (datos sintéticos).

El usuario de prueba se crea con `python seed.py` (desde `01_Software`). Las pruebas automáticas
generan su propia clave y contraseña al azar en cada ejecución.

Las contraseñas se guardan con hash PBKDF2-SHA256. Todas las pantallas y la API (salvo `/login`,
`/api/auth/login` y `/api/health`) requieren sesión iniciada:

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/login` | JSON `{"username", "password"}` → 200 o 401 |
| POST | `/api/auth/logout` | Cierra la sesión |
| GET | `/api/auth/me` | Usuario actual o 401 |

## API de Proveedores

Pantalla web: http://127.0.0.1:8000/proveedores

| Método | Ruta | Respuestas |
|---|---|---|
| GET | `/api/proveedores` | 200 lista ordenada por nombre |
| GET | `/api/proveedores/{id}` | 200 o 404 |
| POST | `/api/proveedores` | JSON `{"nombre"}` → 201, 400 (nombre inválido) o 409 (duplicado) |
| PUT | `/api/proveedores/{id}` | 200, 400, 404 o 409 |
| DELETE | `/api/proveedores/{id}` | 204 o 404 |

Reglas (REQ-001, REQ-012): el nombre se recorta y se compactan los espacios; los duplicados se
detectan sin distinguir mayúsculas y la BD los rechaza con una restricción UNIQUE; solo se aceptan
letras, números, espacios, punto, coma y paréntesis (máx. 100). Los errores internos responden
un mensaje genérico sin detalles.

## Flujo de trabajo Git

1. Tomar un issue y crear una rama: `git checkout -b feat/<tema>`.
2. Commits pequeños y descriptivos.
3. Abrir Pull Request hacia `main` con `Closes #<issue>`; otro integrante lo revisa y aprueba.
4. Nunca hacer push directo a `main`.

## API de licitaciones y ofertas

`GET/POST /api/licitaciones`, `GET/PUT/DELETE /api/licitaciones/{id}`, `PATCH /api/licitaciones/{id}/estado`, `GET/POST /api/ofertas`, `GET/PUT/DELETE /api/ofertas/{id}`. Usar sesión autenticada. 201 para altas, 200 para consultas/ediciones, 204 para bajas, 400 para reglas, 401 sin sesión, 404 inexistente, 409 duplicado/conflicto, 422 estructura inválida. Cierres ISO 8601 con zona horaria.

## Postman

Importar `01_Software/postman/licitaciones.postman_collection.json`, configurar la contraseña sintética local en la variable `password` (no exportarla) y ejecutar en localhost. La colección valida respuestas positivas y negativas con sesión y elimina el proveedor sintético creado.

## Rendimiento local

Desde `01_Software`, instalar `pip install -r requirements-qa.txt` y ejecutar `python performance/run.py`. Crea una BD temporal, inicia Uvicorn en loopback y ejecuta 5 VU durante 30 segundos con Locust. Reportes reales en `04_Evidencias/EV-023-rendimiento/`.
