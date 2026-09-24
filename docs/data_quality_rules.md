# Reglas de calidad de datos

| ID | Campo | Regla | Severidad | Accion |
|---|---|---|---|---|
| DQ001 | customer_id | Debe estar informado | Critica | Cuarentena |
| DQ002 | customer_id | Debe ser unico dentro del lote| Critica | Cuarentena |
| DQ003 | email | Debe estar informado | Alta | Cuarentena |
| DQ004 | email | Debe contener un formato valido | Alta | Cuarentena |
| DQ005 | full_name | Eliminar espacios y normalizar mayusculas | Baja | Corregir |
| DQ006 | country | Utilizar un nombre de pais normalizado | Media | Corregir |
| DQ007 | signup_date | Debe ser una fecha real | Alta | Cuarentena |
| DQ008 | total_spend | Debe convertirse a un valor numerico | Alta | Cuarentena |
| DQ009 | total_spend | Los valores negativos requieren revision | Media | Cuarentena |

## Persistencia en MySQL

- Solo se guarda clean_df que contiene los datos válidos.
- Si introducimos un customer_id que no existía previamente, se inserta.
- Si el cliente ya existe, se actualizan los otros cinco campos con los valores de la nueva carga. total_spend se sustituye, no se suma.
- La última carga válida prevalece.
- Los IDs repetidos dentro del mismo lote siguen yendo a cuarentena.