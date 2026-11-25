# IA-018 · Pruebas de Proveedores y seguridad

| Campo | Valor |
|---|---|
| Herramienta / proveedor | Claude Code / Anthropic |
| Modelo | Claude Sonnet 5.5 |
| Fecha | 2026-11-25 |
| Finalidad | Pruebas (issue #18) |

## Prompt (resumen)

Trabajar el issue #18: pruebas automatizadas de Proveedores y seguridad con pytest, con la salida real como evidencia.

## Salida e incorporado

`01_Software/tests/test_proveedores_seguridad_qa.py` (completo). Ejecución real en `04_Evidencias/EV-018-pytest.txt`.

## Revisión humana

- [x] Oráculos contrastados con REQ-001, REQ-011 y REQ-012
- [x] Datos, límites y aserciones revisados
- [x] Pruebas ejecutadas por el revisor
- Decisión (aprobar / corregir / rechazar): aprobar
- Revisor y fecha: WGuillenDev, 2026-11-25
