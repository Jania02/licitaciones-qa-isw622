# Ambiente de referencia y cómo repetir las verificaciones

Equipo de WGuillenDev, donde se hicieron las verificaciones del issue #2 (2026-11-26). No exige que los demás usen el mismo equipo.

## Commit verificado

| Dato | Valor |
|---|---|
| Candidato de referencia | `543df101618123909f902bc251fb70df29a197cb` (rama `test/23-rendimiento`, PR #42) |
| No incluye | `b798801` (corrección de #32) |
| `main` en la misma fecha | `3074f5c` (solo autenticación) |

El build de entrega es otro dato y se registra al cierre.

## Equipo y versiones

| Elemento | Versión |
|---|---|
| Sistema | Windows 11 Home 10.0.26300, 64 bits |
| Hardware | AMD Ryzen 7 7445HS (6 núcleos, 12 hilos), 15,2 GB de RAM |
| Python / SQLite | 3.14.7 / 3.50.4 |
| FastAPI / Starlette / Pydantic | 0.115.6 / 0.41.3 / 2.14.4 |
| Uvicorn / SQLAlchemy / Jinja2 | 0.34.0 / 2.0.36 / 3.1.5 |
| httpx / itsdangerous | 0.28.1 / 2.2.0 |
| python-dotenv / python-multipart | 1.0.1 / 0.0.20 |
| pytest / Locust / psutil | 8.3.4 / 2.47.0 / 7.2.2 |
| Git | 2.55.0.windows.5 |
| Instalados, sin ejecutar en esta verificación | Postman 12.31.7; Microsoft Edge 158.0.4370.33 |

El README pide Python 3.11 o superior; solo se probó 3.14.7.

## Comandos (PowerShell)

Desde la raíz del repositorio, con el puerto 8000 libre:

```powershell
git fetch origin
git switch --detach 543df101618123909f902bc251fb70df29a197cb
cd 01_Software
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-qa.txt locust==2.47.0 psutil==7.2.2
Copy-Item .env.example .env      # omitir si ya existe un .env propio
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe seed.py --reset      # borra la base de datos configurada
.\.venv\Scripts\python.exe -m locust --version
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Con el servidor en marcha, en otra terminal:

```powershell
foreach ($u in "/api/health","/docs","/login","/api/licitaciones") { "$u " + (curl.exe -s -o NUL -w "%{http_code}" "http://127.0.0.1:8000$u") }
```

## Resultado obtenido el 2026-11-26

| Comprobación | Resultado |
|---|---|
| `pytest` en `543df10` | 80 aprobadas, con avisos de obsolescencia |
| `pytest` en `main` `3074f5c` | 18 aprobadas |
| `seed.py --reset` | Datos sintéticos cargados |
| `/api/health`, `/docs`, `/login` | 200 |
| `/api/licitaciones` sin sesión | 401 |
| `locust --version` | 2.47.0 |

No se ejecutaron la colección de Postman ni la prueba de carga.
