# IA-002 · Datos del proyecto y ambiente de QA

| Campo | Valor |
|---|---|
| Herramienta / proveedor | Claude Code / Anthropic |
| Modelo | Claude Sonnet 5.5 |
| Fecha | 2026-11-26 |
| Finalidad | Planificación QA (issue #2) |

## Prompt (resumen)

Completar los datos del proyecto y del ambiente de QA en Word y Excel, verificando los comandos y las versiones documentadas.

## Salida e incorporado

`02_Proyecto`; Word portada, control de versiones, A1, A2, A4 y A6. Roles tomados de las asignaciones de los issues; criterios de entrada y salida propuestos a partir del enunciado.

## Verificación de comandos (2026-11-26, equipo local)

| Comando | Commit | Resultado |
|---|---|---|
| `pip install -r requirements-qa.txt` en un entorno virtual nuevo | `543df10` | Instalado |
| `pytest -q` | `3074f5c` (main) | 18 aprobadas |
| `pytest -q` | `543df10` | 80 aprobadas |
| `python seed.py --reset` (BD temporal) | `543df10` | Datos cargados |
| `uvicorn app.main:app --port 8765` | `543df10` | `/api/health`, `/docs`, `/login`: 200; `/api/licitaciones` sin sesión: 401 |
| `python -m locust --version` | `543df10` | 2.47.0 |

No se ejecutaron la colección de Postman ni la prueba de carga. Las versiones de hardware, sistema y herramientas se leyeron del equipo de WGuillenDev; los demás integrantes pueden usar otro ambiente.

## Revisión humana

- [ ] Nombres, roles y responsables confirmados
- [ ] Ambiente, versiones y criterios revisados
- [ ] Coincidencia entre 02_Proyecto y el Word verificada
- Decisión (aprobar / corregir / rechazar): pendiente
- Revisor y fecha: pendiente

## Seguimiento 2026-11-26: datos confirmados y ambiente de referencia

Prompt (resumen): completar curso, entrega prevista, integrantes y roles confirmados por WGuillenDev; documentar su equipo como ambiente de referencia con versiones y comandos repetibles.

Incorporado: `02_Proyecto`, portada, A1, A4 y A6; usuarios de GitHub en el repositorio (nombres completos y correos solo en la copia de entrega); `docs/qa/ambiente_referencia.md`. Los comandos se repitieron en una copia limpia de `543df10`: 80 aprobadas, datos cargados, respuestas 200 y 401 esperadas y Locust 2.47.0.

Los criterios de entrada y salida siguen como **propuestos**. Revisión humana: **pendiente**.
