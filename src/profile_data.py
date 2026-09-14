from pathlib import Path

import pandas as pd

from src.pipeline import process_customers


DATA_PATH = Path("data/raw/customers_sample.csv")

df = pd.read_csv(DATA_PATH, sep=";")

clean_df, quarantine_df = process_customers(df)

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
