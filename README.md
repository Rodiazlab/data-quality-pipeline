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
- `data/metrics`: resúmenes de calidad por ejecución, generados localmente y excluidos de Git.

## Tecnologias

- Python
- pandas
- SQL
- Streamlit
- Git
- Scrum

## Estado

- Sprint 1 completado: validación y limpieza ✅
- Sprint 2 completado: clasificación e integración ✅
- Pipeline reutilizable mediante `process_customers()` ✅
- Separación entre `clean` y `quarantine` ✅
- 21 tests automáticos, incluido uno de integración ✅
- Persistencia en SQL: carga en MySQL está integrada con éxito, permite insertar nuevos clientes y actualizar los ya existentes.
- La insercción, actualización y repetición de la carga se han comprobado manualmente en MySQL.
- Métricas de calidad: recuentos de registros recibidos, válidos y en cuarentena, porcentajes e incidencias por motivo.
- Resumen de calidad guardado en un archivo JSON distinto por ejecución.
- Pruebas manuales del guardado: dos ejecuciones generan dos resúmenes y conservan el historial.
- Sprint 3 completado: persistencia en MySQL e integración con el pipeline ✅
- Sprint 4 completado: métricas de calidad, resumen JSON por ejecución y tests ✅
- Sprint 5 completado: lectura de archivos JSON y visualización en Streamlit.

## Instalación y tests

Desde la carpeta raíz del proyecto, crea y activa un entorno virtual en macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecuta los tests:

```bash
python -m pytest -v
```

Los tests utilizan una conexión MySQL simulada, por lo que no necesitan una base de datos activa.

## Configuración de MySQL y ejecución

Para ejecutar el pipeline completo necesitas un servidor MySQL activo.

1. Crea una base de datos y, dentro de ella, ejecuta el script `sql/create_customers.sql` para crear la tabla `customers`.

2. Copia `.env.example` a un archivo llamado `.env` y configura:
   - `DB_HOST`: dirección del servidor.
   - `DB_PORT`: puerto de MySQL.
   - `DB_USER`: usuario con permisos sobre la base de datos.
   - `DB_PASSWORD`: contraseña del usuario.
   - `DB_NAME`: nombre de la base de datos creada.

   El archivo `.env` contiene credenciales locales y está excluido de Git.

3. Con el entorno virtual activado, ejecuta desde la raíz del proyecto:

   ```bash
   python -m src.profile_data
   ```

El pipeline lee `data/raw/customers_sample.csv`, genera los CSV de datos válidos y cuarentena, guarda un resumen JSON en `data/metrics` y carga los registros válidos en MySQL.

Cada ejecución genera un JSON con un nombre distinto. Los clientes existentes se actualizan por `customer_id`

## Datos de ejemplo

El archivo `data/raw/customers_sample.csv` contiene datos ficticios creados para probar las reglas de calidad. No contiene información de clientes reales.

## Panel de calidad con Streamlit

El panel permite seleccionar una ejecución y consultar:

- Registros recibidos, válidos y en cuarentena.
- Porcentajes de validez y cuarentena.
- Incidencias por motivo.

Lee los archivos `quality_summary_*.json` de `data/metrics/`.
Si una ejecución no tiene incidencias, muestra un mensaje en lugar del gráfico.

### Ejecutar el panel

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Para detenerlo, pulsa Control + C en la terminal.

Es necesario ejecutar primero el pipeline para generar las métricas.