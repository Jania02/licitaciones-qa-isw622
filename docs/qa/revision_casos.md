# Revisión humana de las fichas (IA-005)

**Decisión:** aprobadas las 23 fichas por WGuillenDev el 2026-11-26 sobre `6333579`.

Comparación de `05_Casos` entre la versión aprobada (`756b40d`) y la actual. 

Cambios comunes a CP-001 a CP-022: se llenó **Técnica**; **Precondiciones** y **Datos** dejan de repetir el mismo texto; los pasos quedan numerados; el oráculo cita su REQ; se agregó IA-005; la aprobación anterior queda en Notas. **Modo** se llenó donde estaba vacío (todos salvo CP-010 a CP-012).

| CP | REQ | Qué cambió en particular | Resultado esperado |
|---|---|---|---|
| CP-001 | REQ-001 | Tres nombres exactos; agrega comparación con uno distinto | Clave de A igual a la de B y distinta de la de C |
| CP-002 | REQ-001 | Agrega el alta válida de P1 antes del duplicado | 201, luego 409; queda un solo proveedor |
| CP-003 | REQ-012 | Agrega un nombre válido de control | Rechaza "Norte@Sur"; acepta el control |
| CP-004 | REQ-012 | Rutas de interfaz y API; texto escapado | 400 en ambas; sin alerta; nada guardado |
| CP-005 | REQ-012 | Fallo provocado y texto sintético definidos | 500 genérico, sin traza, rutas ni el texto |
| CP-006 | REQ-013 | Define las 4 tareas y participantes U1 y U2; tiempos y obstáculos pasan a los pasos | Al menos 3 de 4 tareas sin ayuda |
| CP-007 | REQ-011 | Datos de L1; reinicio sin borrar la BD; sin registros previos | Se recuperan los tres registros iguales |
| CP-008 | REQ-002 | Datos exactos de L1 y del código repetido | Publicada; repetido 409; una sola |
| CP-009 | REQ-003 | Las 9 combinaciones de estado | Solo 3 transiciones; 6 rechazadas |
| CP-010 | REQ-004 | Datos iguales a los del script (CRC 100,00, antes L1); agrega la vía API | 400 en ambas; nada guardado |
| CP-011 | REQ-004 | Datos iguales a los del script | 400 en Borrador y en Cerrada; nada guardado |
| CP-012 | REQ-005 | Se explicitan los rechazos | Solo acepta 10 000 000,00 |
| CP-013 | REQ-006 | Montos de ambas ofertas; sin ofertas previas | 409 y error de integridad; queda la primera |
| CP-014 | REQ-011 | Cuerpo exacto de la solicitud | 201 y 200 con los mismos datos |
| CP-015 | REQ-011, REQ-005 | Id 999999; antes decía "4xx" | 400 y 404; nada guardado |
| CP-016 | REQ-007 | Tres conjuntos de datos A, B y C | "Sin ofertas válidas"; 9 000 000; la primera |
| CP-017 | REQ-008 | Cada oferta se evalúa por separado | 10 % conveniente; 5 % aceptable; 0 % válida sin ahorro |
| CP-018 | REQ-009 | Agrega CRC 0,01 y el rango traslapado | Aprobador por rango; traslape rechazado |
| CP-019 | REQ-010 | Pasos de ida y vuelta CRC y USD | USD 18 000,00 con tasa y fecha; CRC intacto |
| CP-020 | REQ-014 | Perfil de carga y endpoint | p95 ≤ 1 500 ms; errores ≤ 5 %; CPU y RAM |
| CP-021 | REQ-002 | Datos base y una variación por intento; **agrega publicar una licitación vencida** | 400 en las tres altas, sin guardar; publicar la vencida: 400 y sigue en Borrador |
| CP-022 | REQ-010 | Tasa vigente 500 definida | 400 en ambas; sigue 500 |
| CP-023 | REQ-004 | **Caso nuevo**: antes y después del cierre | Antes se acepta; después 400 |

## Alcance

- Las rutas y los códigos HTTP salen del código de los PR #32 a #42, no del enunciado.
