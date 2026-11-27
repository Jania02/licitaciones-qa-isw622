# IA-004 · Registro de riesgos

| Campo | Valor |
|---|---|
| Herramienta / proveedor | Claude Code / Anthropic |
| Modelo | Claude Sonnet 5.5 |
| Fecha | 2026-11-26 |
| Finalidad | Planificación QA: riesgos del proyecto (issue #4) |

## Prompt (resumen)

1. Completar el issue #4: conservar los riesgos existentes y llegar al menos a tres, con probabilidad, impacto, prevención y contingencia, iguales en 08_Riesgos y Word A9. Marcar si se materializaron solo con evidencia.
2. Ajustar la altura de la fila de RSK-001, corregir los vínculos y el responsable de RSK-003 y RSK-004 sin dar por probado lo que no se ejecutó, y registrar este uso de IA.

## Salida e incorporado

`08_Riesgos` y Word A9: RSK-002, RSK-003 y RSK-004 (texto, probabilidad, impacto, mitigación, contingencia, responsable y vínculos propuestos por la IA). RSK-001 conserva sus datos; solo cambia la altura de su fila.

## Cobertura de las pruebas existentes

Revisadas leyendo el código; no se ejecutaron en esta intervención.

| Riesgo | Prueba relacionada | Qué cubre | Qué no cubre |
|---|---|---|---|
| RSK-003 | `test_conversion` y `test_moneda_no_cambia_importes` en `test_evaluacion_moneda.py` (PR #40, borrador) | Conversión 9 000 000 / 500, rechazo de tasa 0 y licitaciones sin cambios al consultar en USD | Caída, tiempo de espera o respuesta inválida del servicio externo (`/api/tasas/externa`); tasa negativa |
| RSK-004 | `test_error_interno_no_expone_detalles` en `test_proveedores_api.py` (PR #32, CP-005) | Un error interno provocado responde 500 genérico sin el detalle de la excepción | Secretos o datos personales publicados en el repositorio, la IA o las evidencias |

## Revisión humana

- [ ] Riesgos contrastados con el enunciado y el plan del equipo
- [ ] Probabilidad, impacto, mitigación, contingencia y responsables revisados
- [ ] Coincidencia entre 08_Riesgos y Word A9 verificada
- Decisión (aprobar / corregir / rechazar): pendiente
- Revisor y fecha: Jania02, pendiente
