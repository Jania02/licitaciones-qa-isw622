# Requisitos (hoja 03_Requisitos, Word A3)

Criterios resumidos del enunciado, sección 3. La prioridad es una propuesta.

| ID | Área | Criterio de aceptación | Prioridad | Casos |
|---|---|---|---|---|
| REQ-001 | Proveedores | Crear, editar y listar; nombres equivalentes tras recortar, compactar espacios e ignorar mayúsculas se rechazan | Alta | CP-001, CP-002 |
| REQ-002 | Licitaciones | Código único sin distinguir mayúsculas ni espacios laterales; título no vacío, presupuesto > 0 y cierre futuro al crear o publicar | Alta | CP-008, CP-021 |
| REQ-003 | Estados | Solo Borrador → Publicada o Cerrada y Publicada → Cerrada | Alta | CP-009 |
| REQ-004 | Vencimiento | Ofertas solo en Publicadas y antes del cierre; exactamente en el cierre se rechazan | Alta | CP-010, CP-011 |
| REQ-005 | Montos | 0 < oferta ≤ presupuesto | Alta | CP-012 |
| REQ-006 | Duplicados | Una oferta por proveedor y licitación, rechazada también por la base de datos | Alta | CP-013 |
| REQ-007 | Mejor oferta | Gana la menor; en empate, la primera registrada; sin ofertas: "Sin ofertas válidas" | Alta | CP-016 |
| REQ-008 | Ahorro | ((presupuesto − mejor) / presupuesto) × 100; ≥10 % conveniente, >0 y <10 % aceptable, 0 % válida sin ahorro | Media | CP-017 |
| REQ-009 | Aprobación | 0,01–999 999,99 Encargado de área; 1 000 000–9 999 999,99 Gerencia; ≥10 000 000 Junta Directiva; sin traslapes | Media | CP-018 |
| REQ-010 | Moneda | Solo se guardan CRC; USD = CRC / tasa, tasa > 0; mostrar tasa y fecha; alternar no modifica la BD | Media | CP-019, CP-022 |
| REQ-011 | Persistencia y API | Los datos persisten al reiniciar; la API responde éxito y error y valida igual que la interfaz | Alta | CP-007, CP-014, CP-015 |
| REQ-012 | Seguridad | Nombre solo con letras, números, espacios, punto, coma y paréntesis; sin ejecución HTML/script ni errores internos visibles | Alta | CP-003, CP-004, CP-005 |
| REQ-013 | Usabilidad | Con 2 personas ajenas, al menos 3 de 4 tareas sin ayuda | Media | CP-006 |
| REQ-014 | Rendimiento | 5 usuarios, 30 s, GET de listado local: p95 ≤ 1 500 ms y errores ≤ 5 %; registrar CPU/RAM | Media | CP-020 |
