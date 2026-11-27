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

- [ ] Oráculos contrastados con el enunciado
- [ ] Entradas, límites y pasos de las 23 fichas revisados
- [ ] Word A3, A5 y A10 coinciden con 05_Casos
- Decisión (aprobar / corregir / rechazar): pendiente
- Revisor y fecha: pendiente

La aprobación registrada en IA-003 corresponde a las fichas del commit `756b40d`; no cubre estos cambios. Por eso las fichas quedan en `Pendiente` / `En revisión`.
