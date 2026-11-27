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

| IA | Archivo | Revisión humana vigente |
|---|---|---|
| IA-002 | `IA-002_datos_proyecto.md` | Aprobada (WGuillenDev, 2026-11-26, `7134063`) |
| IA-003 | `IA-003_requisitos.md` | Historial: aprobada el 2026-11-25 (criterios, prioridades y casos, sobre `756b40d`); las fichas actuales las cubre IA-005 |
| IA-004 | `IA-004_riesgos.md` | **Pendiente** (Jania02) |
| IA-005 | `IA-005_fichas_casos.md` | Aprobada (WGuillenDev, 2026-11-26, `6333579`) |
| IA-018 | `IA-018_pruebas_proveedores.md` (PR #44) | Seguimiento aprobado (WGuillenDev, 2026-11-26, `d8cfb82`); la aprobación inicial queda como historial |
| IA-025 | `IA-025_bug_001.md` (PR #45) | Aprobada (WGuillenDev, 2026-11-25) |
| IA-048 | `IA-048_ejecuciones.md` | Aprobada (WGuillenDev, 2026-11-26, `106ab75`) |
| IA-049 | `IA-049_usos_ia.md` | Corregida y aprobada (WGuillenDev, 2026-11-26) |

## Totales en `10_Revision_IA`

| Grupo | Filas |
|---|---|
| Total | 54 |
| Revisiones vigentes (`01_Resumen`) | 30: 23 de IA-005, 3 de IA-025 y 1 de IA-002, IA-018, IA-048 e IA-049 |
| Historial | 23: 22 de IA-003 y 1 de IA-018 |
| Pendientes | 1: IA-004 |

Los identificadores `REV-###` se conservan; quedan saltos donde se retiraron las filas de IA-018 ligadas a casos. Los controles que un registro no declara siguen en `Pendiente`.

## Revisión humana

- [x] Hojas 09 y 10 contrastadas con los archivos de `05_IA`
- Decisión (aprobar / corregir / rechazar): corregir y aprobar
- Revisor y fecha: WGuillenDev, 2026-11-26
- Versión revisada: `5e9aa43`
- Corrección pedida y aplicada: una sola fila para el seguimiento de IA-018, vinculada a REQ-001, REQ-011, REQ-012 y EV-018; se retira la relación inferida con CP-001, CP-002 y CP-004 (también la de CP-003); las revisiones anteriores se conservan como historial.

## Controles confirmados (2026-11-26)

WGuillenDev confirmó las aserciones y los datos de IA-005 y los controles del seguimiento de IA-018 (su registro está en el PR #44). Actualizados en `10_Revision_IA`. Después confirmó el oráculo y los datos de IA-002, IA-048 e IA-049, también actualizados en `10_Revision_IA`.
