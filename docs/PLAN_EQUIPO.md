# Plan de trabajo del equipo — Práctica Integradora QA (ISW-622)

Sistema de Gestión de Licitaciones · Python + FastAPI + SQLite + pytest

> Reemplazar "Integrante 1/2/3" por los nombres reales y sus usuarios de GitHub.

| Rol | Nombre | GitHub |
|---|---|---|
| Integrante 1 — Coordinación, Proveedores, Seguridad, Usabilidad | | |
| Integrante 2 — Licitaciones, Ofertas, API, Defecto BUG-001 | | |
| Integrante 3 — Evaluación, Tipo de cambio, Rendimiento, IA/Evidencias | | |

## Criterio de la división

El enunciado exige que **todos** programen, revisen código, diseñen/ejecuten pruebas y defiendan.
Por eso cada persona tiene un **módulo de código + sus pruebas + un tipo de prueba especial + una parte de la documentación**,
y cada PR lo revisa otra persona del equipo.

## Integrante 1 — Coordinación · Proveedores · Seguridad · Usabilidad

| Tipo | Tarea | REQ |
|---|---|---|
| Código | Esqueleto del proyecto, autenticación (usuario/contraseña) | — |
| Código | Proveedores: crear, listar, editar, eliminar; normalización y duplicados; validación de caracteres; escape HTML | REQ-001, REQ-012 |
| Código | Seed de datos sintéticos (P1, P2, L1, ofertas, tipo de cambio) y script de reinicio de BD; README | REQ-011 |
| Pruebas | Unitarias y de integración de Proveedores; CP de seguridad (≥2) | REQ-001, REQ-012 |
| QA especial | Sesión de usabilidad: 2 personas ajenas al equipo, 2 tareas cada una | REQ-013 |
| Documentos | Excel 02_Proyecto, 03_Requisitos, 08_Riesgos, 13_Seguridad, 14_Usabilidad · Word portada y Parte A | |
| Cierre | Revisar 01_Resumen, que Word y Excel coincidan; exportar PDF y armar ZIP final | |

## Integrante 2 — Licitaciones · Ofertas · API · BUG-001

| Tipo | Tarea | REQ |
|---|---|---|
| Código | Licitaciones: CRUD, código único normalizado, validaciones, transición de estados | REQ-002, REQ-003 |
| Código | Ofertas: registrar/listar por licitación y proveedor; monto, plazo, estado; restricción UNIQUE en BD | REQ-004, REQ-005, REQ-006 |
| Código | API HTTP (≥4 operaciones: consulta, alta y escenarios negativos) con errores controlados | REQ-011 |
| Pruebas | Unitarias de reglas de licitación/oferta; integración API (TestClient); casos límite (0, negativo, igual, +0,01; exactamente al cierre) | REQ-002–006, REQ-011 |
| QA especial | Defecto inducido BUG-001 en rama `lab/bug-001` (aceptar oferta exactamente al cierre), retest y ≥2 regresiones; guardar los dos hashes | — |
| Documentos | Excel 05_Casos (consolida los 20 CP), 06_Ejecuciones (≥23 RUN), 07_Defectos · Word Parte B | |

## Integrante 3 — Evaluación · Tipo de cambio · Rendimiento · IA/Evidencias

| Tipo | Tarea | REQ |
|---|---|---|
| Código | Evaluación: mejor oferta (empate → la primera), "Sin ofertas válidas", ahorro %, clasificación | REQ-007, REQ-008 |
| Código | Aprobadores por rangos configurables (tabla con CRUD) | REQ-009 |
| Código | Tipo de cambio: configuración manual + servicio externo; alternar CRC/USD sin tocar la BD; mostrar tasa y fecha | REQ-010 |
| Pruebas | Unitarias de evaluación/ahorro/aprobador/conversión (escenarios 10 % / 5 % / 0 %); colección Postman | REQ-007–010 |
| QA especial | Prueba de carga con Locust: 5 VU, 30 s, GET de listado; p95, errores, CPU/RAM | REQ-014 |
| Documentos | Excel 09_IA_Usos, 10_Revision_IA, 11_Evidencias, 12_Automatizacion, 15_Rendimiento · Word Partes C y D | |

## Reglas para todos

- **Nunca** hacer commit directo a `main`. Rama por issue: `feat/proveedores`, `test/ofertas-api`, `docs/plan-qa`, etc.
- Cada PR lo revisa y aprueba **otro integrante** antes de hacer merge. El PR menciona `Closes #N`.
- Cada integrante necesita **al menos 2 commits no consecutivos** en el historial (en la práctica serán muchos más).
- Cada integrante registra **al menos 1 IA-###** (prompt + salida saneados en `05_IA/`) y su revisión humana.
- El resultado esperado de cada CP sale de los REQ del enunciado, **no** de lo que diga la IA.
- No subir contraseñas, tokens ni datos personales. Usar `.env.example` para la configuración.
- Todos deben poder ejecutar la app y las pruebas, y explicar las reglas principales en la defensa.

## Mínimos cuantitativos (control)

| Elemento | Mínimo | Responsable de consolidar |
|---|---|---|
| REQ con prioridad y ≥1 CP | 14 | Integrante 1 |
| CP-### | 20 (≥7 unit, ≥3 integración/API, ≥4 funcionales, ≥2 seguridad, ≥1 usabilidad, ≥1 rendimiento, 2 borde/negativo) | Integrante 2 |
| RUN | ≥23 (20 iniciales + ≥3 reejecuciones) | Integrante 2 |
| Pruebas automatizadas | ≥8 (≥5 unitarias, ≥2 integración/API) | Integrante 3 |
| BUG | ≥1 con antes/después | Integrante 2 |
| RSK | ≥3 | Integrante 1 |
| IA-### | ≥3 (código, pruebas, revisión/diagnóstico) | Integrante 3 |
| Usabilidad | 2 participantes × 2 tareas | Integrante 1 |
| Rendimiento | 1 ejecución 5 VU / 30 s | Integrante 3 |
| Seguridad | ≥2 escenarios | Integrante 1 |

Reparto sugerido de los 20 CP: Integrante 1 → 7 (proveedores, seguridad, usabilidad, persistencia) ·
Integrante 2 → 8 (licitaciones, estados, ofertas, API, límites) · Integrante 3 → 5 (evaluación, moneda, rendimiento).

## Orden de trabajo (milestones en GitHub)

1. **Paso 1 · Preparación** — repo, esqueleto, roles, ambiente.
2. **Paso 2 · Planificación QA** — REQ, riesgos, CP, Word Parte A (antes de probar).
3. **Paso 3 · IA y desarrollo** — módulos, seed, registros IA.
4. **Paso 4 · Ejecución** — automatizadas, API, funcionales, seguridad, usabilidad, rendimiento.
5. **Paso 5 · Inconformidades** — BUG-001, retest, regresión.
6. **Paso 6 · Informe/cierre** — Word B/C/D, resumen, PDF, ZIP, ensayo de defensa.
