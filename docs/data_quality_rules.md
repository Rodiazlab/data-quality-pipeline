# Reglas de calidad de datos

| ID | Campo | Regla | Severidad | Accion |
|---|---|---|---|---|
| DQ001 | customer_id | Debe estar informado | Critica | Cuarentena |
| DQ002 | customer_id | Debe ser unico | Critica | Cuarentena |
| DQ003 | email | Debe estar informado | Alta | Cuarentena |
| DQ004 | email | Debe contener un formato valido | Alta | Cuarentena |
| DQ005 | full_name | Eliminar espacios y normalizar mayusculas | Baja | Corregir |
| DQ006 | country | Utilizar un nombre de pais normalizado | Media | Corregir |
| DQ007 | signup_date | Debe ser una fecha real | Alta | Cuarentena |
| DQ008 | total_spend | Debe convertirse a un valor numerico | Alta | Cuarentena |
| DQ009 | total_spend | Los valores negativos requieren revision | Media | Cuarentena |
