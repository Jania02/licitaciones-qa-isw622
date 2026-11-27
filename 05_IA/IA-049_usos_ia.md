# IA-049 · Registro y verificación de usos de IA

| Campo | Valor |
|---|---|
| Herramienta / proveedor | Claude Code / Anthropic |
| Modelo | Claude Sonnet 5.5 |
| Fecha | 2026-11-26 |
| Finalidad | Documentación y revisión de usos de IA (issue #49) |

## Prompt (resumen)

Verificar IA-003, IA-004, IA-018 e IA-025, comprobar que coincidan los archivos de `05_IA` con las hojas `09_IA_Usos` y `10_Revision_IA`, y registrar el estado real de cada revisión humana.

## Salida e incorporado

Hojas `09_IA_Usos` y `10_Revision_IA`, incluidos los registros nuevos IA-002, IA-005, IA-048 e IA-049.

## Verificación de los registros

Todos tienen herramienta, proveedor, modelo, fecha, finalidad, prompt, salida o partes incorporadas y decisión. Los prompts son **resúmenes saneados**, no transcripciones; las salidas se identifican por los archivos y commits incorporados.

| IA | Archivo | Revisión humana |
|---|---|---|
| IA-002 | `IA-002_datos_proyecto.md` | Pendiente |
| IA-003 | `IA-003_requisitos.md` | Aprobada (WGuillenDev, 2026-11-25): criterios, prioridades y casos, sobre las fichas de `756b40d`. No declara revisión de 06, 07, 08, 11 ni Word B5, llenados con la misma herramienta. |
| IA-004 | `IA-004_riesgos.md` | Pendiente (Jania02) |
| IA-005 | `IA-005_fichas_casos.md` | Pendiente |
| IA-018 | `IA-018_pruebas_proveedores.md` (PR #44) | Parte inicial aprobada (WGuillenDev, 2026-11-25); seguimiento aprobado (WGuillenDev, 2026-11-26, `d8cfb82`) |
| IA-025 | `IA-025_bug_001.md` (PR #45) | Aprobada (WGuillenDev, 2026-11-25) |
| IA-048 | `IA-048_ejecuciones.md` | Pendiente |
| IA-049 | `IA-049_usos_ia.md` | Pendiente |

## Revisión humana

- [ ] Hojas 09 y 10 contrastadas con los archivos de `05_IA`
- Decisión (aprobar / corregir / rechazar): pendiente
- Revisor y fecha: pendiente

## Seguimiento 2026-11-26: historial, EV-018 y trazabilidad

- `10_Revision_IA`: las 22 aprobaciones de IA-003 y la aprobación inicial de IA-018 para CP-003 quedan marcadas como historial. `01_Resumen` cuenta 6 revisiones vigentes (3 de IA-018 y 3 de IA-025).
- `11_Evidencias`: EV-018 (`04_Evidencias/EV-018-pytest-tras-pr32.txt`, PR #44). La suite en `2d46001` reprodujo 98 aprobadas el 2026-11-26.
- `09_IA_Usos`: trazabilidad completa de IA-003.

Revisión humana: **pendiente**.

## Seguimiento 2026-11-26: aprobación de IA-018

WGuillenDev confirmó la aprobación del seguimiento de IA-018 registrada en `d8cfb82`. Se refleja en `09_IA_Usos` y `10_Revision_IA`, enlazada con el registro y con EV-018. `01_Resumen` cuenta 7 revisiones vigentes (4 filas de IA-018 y 3 de IA-025). La relación de IA-018 con CP-001 a CP-004 es inferida por requisito.

Revisión humana de IA-049: **pendiente**.
