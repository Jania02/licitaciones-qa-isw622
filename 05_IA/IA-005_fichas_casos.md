# IA-005 · Fichas de los casos de prueba

| Campo | Valor |
|---|---|
| Herramienta / proveedor | Claude Code / Anthropic |
| Modelo | Claude Sonnet 5.5 |
| Fecha | 2026-11-26 |
| Finalidad | Diseño de pruebas (issues #5, #6 y #7) |

## Prompt (resumen)

Continuar el PR #46: verificar que las fichas cumplan los criterios de los issues #5, #6 y #7 y completar lo que falte.

## Salida e incorporado

- `05_Casos`: técnica y modo en las fichas; precondiciones y datos exactos separados (antes repetían el mismo texto); pasos y oráculo precisados a partir de los REQ. Las rutas y códigos HTTP salen del código de los PR abiertos (#32 a #42).
- CP-023 nuevo: oferta antes y después del cierre (faltaba en el #6).
- `03_Requisitos` (REQ-004), `docs/qa/requisitos.md`, Word A3, A5 y A10 (CP-010).

No se ejecutó ningún caso en esta intervención.

## Revisión humana

- [x] Oráculos contrastados con el enunciado
- [x] Entradas, límites y pasos de las 23 fichas revisados
- [x] Word A3, A5 y A10 coinciden con 05_Casos
- Decisión (aprobar / corregir / rechazar): aprobar
- Revisor y fecha: WGuillenDev, 2026-11-26
- Versión revisada: `6333579`

La aprobación registrada en IA-003 corresponde a las fichas del commit `756b40d`; queda como historial. Las fichas actuales están aprobadas por esta revisión.

## Seguimiento 2026-11-26: preparación de la revisión

Incorporado: trazabilidad de IA-003; historial de la aprobación anterior en las notas de `05_Casos`; `01_Resumen` cuenta solo aprobaciones vigentes; precondiciones precisadas en CP-007 y CP-013; guía `docs/qa/revision_casos.md`. Revisión humana: aprobada sobre `6333579` (ver arriba).

## Seguimiento 2026-11-26: CP-021 y verificación

Prompt (resumen): completar CP-021 con el intento de publicar una licitación vencida y verificar las 23 fichas y Word A3, A5 y A10.

Incorporado: paso y oráculo de publicación vencida en CP-021 (título, `03_Requisitos` y `docs/qa/requisitos.md`); en Word A5, CP-011 pasa a figurar como automatizado. Comprobación por script de requisitos, tipos, A3, A5 y A10 contra `05_Casos`. No se ejecutó ningún caso. Revisión humana: aprobada sobre `6333579` (ver arriba).

## Controles confirmados (2026-11-26)

WGuillenDev confirmó las aserciones (resultados esperados) y los datos de las 23 fichas. Constan como `Sí` en `10_Revision_IA`; la ejecución no aplica porque los casos no se ejecutaron en esta intervención.
