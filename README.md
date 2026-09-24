# Data Quality Pipeline

Proyecto de ingenieria y calidad de datos orientado a transformar datos brutos e inconsistentes en informacion fiable, validada y preparada para su consumo.

## Objetivo

Construir un pipeline reproducible que permita:

- Ingerir datos desde diferentes fuentes.
- Detectar valores ausentes, duplicados y formatos invlidos.
- Limpiar y normalizar los datos.
- Separar los registros validos de los registros problemticos.
- Cargar los datos validados en una base de datos SQL.
- Medir y visualizar la calidad de los datos.

## Arquitectura

El proyecto utiliza las siguientes capas:

- `raw`: datos originales sin modificar.
- `clean`: datos que cumplen las reglas de calidad.
- `quarantine`: registros que necesitan revision.
- `src`: codigo del pipeline.
- `tests`: pruebas automaticas.
- `sql`: modelos y consultas SQL.
- `docs`: documentacion tecnica y Scrum.

## Tecnologias

- Python
- pandas
- SQL
- Power BI
- Git
- Scrum

## Estado

- Sprint 1 completado: validación y limpieza ✅
- Sprint 2 completado: clasificación e integración ✅
- Pipeline reutilizable mediante `process_customers()` ✅
- Separación entre `clean` y `quarantine` ✅
- 15 tests automáticos, incluido uno de integración ✅
- Persistencia en SQL: carga en MySQL está integrada con éxito, permite insertar nuevos clientes y actualizar los ya existentes.
- La insercción, actualización y repetición de la carga se han comprobado manualmente en MySQL.
