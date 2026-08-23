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

Proyecto en desarrollo.
