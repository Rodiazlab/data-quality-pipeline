from pathlib import Path

import pandas as pd

from src.pipeline import process_customers

from src.persistence import connect_to_database, save_customers

from src.metrics import build_quality_summary, save_quality_summary

from uuid import uuid4


DATA_PATH = Path("data/raw/customers_sample.csv")
METRICS_DIR = Path("data/metrics")
METRICS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH, sep=";")

clean_df, quarantine_df = process_customers(df)
quality_summary = build_quality_summary(df, clean_df, quarantine_df)
run_id = uuid4().hex
summary_path = METRICS_DIR / f"quality_summary_{run_id}.json"
save_quality_summary(quality_summary, summary_path)
print(f"\nResumen de calidad guardado en: {summary_path}")

print("\nMÉTRICAS DE CALIDAD")
print(quality_summary)

print("DIMENSIONES")
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")

print("\nTIPOS DE DATOS")
print(df.dtypes)

print("\nVALORES AUSENTES")
print(df.isna().sum())

print("\nFILAS EXACTAMENTE DUPLICADAS")
print(df.duplicated().sum())

print("\nIDENTIFICADORES REPETIDOS")
print(df["customer_id"].duplicated(keep=False).sum())

print("\nCOMPLETITUD POR COLUMNA (%)")
completeness = (1 - df.isna().mean()) * 100
print(completeness.round(2))


print("\nRESUMEN DE CLASIFICACION")
print(f"Registros validos: {len(clean_df)}")
print(f"Registros en cuarentena: {len(quarantine_df)}")



print("\nDATOS VALIDOS")
print(clean_df)


CLEAN_PATH = Path("data/clean/customers_clean.csv")
QUARANTINE_PATH = Path("data/quarantine/customers_quarantine.csv")


print("\nDATOS EN CUARENTENA CON MOTIVOS")
print(quarantine_df)

clean_df.to_csv(
    CLEAN_PATH,
    sep=";",
    index=False,
)

quarantine_df.to_csv(
    QUARANTINE_PATH,
    sep=";",
    index=False,
)

print(f"\nArchivo limpio creado: {CLEAN_PATH}")
print(f"Archivo de cuarentena creado: {QUARANTINE_PATH}")

connection = connect_to_database()

try:
    save_customers(connection, clean_df)
finally:
    connection.close()