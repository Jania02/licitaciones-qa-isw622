# IA-050 · Ejecución de pruebas y registro de resultados

| Campo | Valor |
|---|---|
| Herramienta / proveedor | Claude Code / Anthropic |
| Modelo | Claude Sonnet 5.5 |
| Fecha | 2026-11-26 |
| Finalidad | Ejecutar los casos de prueba, guardar la evidencia real y completar las hojas del Excel y del Word |
| Datos compartidos | Sintéticos (P1, P2, L1); sin secretos ni datos personales |

## Prompt (resumen)

Completar lo que falta para cumplir la práctica: ejecutar los casos automatizados y funcionales, registrar cada RUN con su evidencia, completar las hojas 04, 06, 11, 12, 13 y 15 y el Word, sin inventar resultados.

## Salida e incorporado

- `01_Software/qa_scripts/ejecutar_casos_pytest.py` y `ejecutar_casos_funcionales_api.py`.
- Evidencias `EV-030` a `EV-052` en `04_Evidencias/`: salida real de cada ejecución, con fecha, commit y entorno.
- Excel: RUN-005 a RUN-027, hojas 04, 11, 12, 13, 15 y cierre de 01_Resumen.

## Límites declarados

- Los casos CP-007, CP-008, CP-019, CP-021 y CP-022 se ejecutaron por API sobre un servidor local con base temporal; no sustituyen una prueba manual en el navegador.
- CP-006 (usabilidad) **no se ejecutó**: requiere 2 personas ajenas al equipo. La hoja 14_Usabilidad queda vacía a propósito.
- CP-020 se registra con la evidencia existente `EV-023` (ejecución del equipo), no se repitió.
- La colección de Postman no se ejecutó para este registro.

## Revisión humana

**Pendiente.** Un integrante debe revisar los scripts, repetir al menos una ejecución y registrar su decisión en `10_Revision_IA` (REV-058). Hasta entonces la decisión en `09_IA_Usos` es "Pendiente".
