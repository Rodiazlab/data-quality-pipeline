from pathlib import Path

import pandas as pd

from src.validation import (
    find_duplicates,
    find_invalid_emails,
    find_missing_values,
)

from src.cleaning import (
     normalize_amounts,
     parse_mixed_dates,
)

from src.classification import classify_records



DATA_PATH = Path("data/raw/customers_sample.csv")

df = pd.read_csv(DATA_PATH, sep=";")

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

missing_customer_id = df["customer_id"].isna()

print("\nREGISTROS SIN CUSTOMER_ID")
print(df[missing_customer_id])

missing_email = df["email"].isna()

print("\nREGISTROS SIN EMAIL")
print(df[missing_email])

duplicated_customer_id = df["customer_id"].duplicated(keep=False)

print("\nREGISTROS CON CUSTOMER DUPLICADO")
print(df[duplicated_customer_id]) 

invalid_email = find_invalid_emails(
    df,
    "email",
)

print("\nREGISTROS CON EMAIL INVALIDO")
print(df[invalid_email])

parsed_dates = parse_mixed_dates(
    df,
    "signup_date",
)

invalid_signup_date = parsed_dates.isna()

print("\nREGISTROS CON FECHA INVALIDO")
print(df[invalid_signup_date])

parsed_amounts = normalize_amounts(
    df,
    "total_spend",
) 

quality_issues = classify_records(
    df,
    parsed_dates,
    parsed_amounts,
)

amount_comparison = pd.DataFrame(
    {
        "original": df["total_spend"],
        "normalizado": parsed_amounts,
    }
)

print("\nCOMPARACION DE IMPORTES")
print(amount_comparison)

negative_amount = parsed_amounts < 0
invalid_amount = parsed_amounts.isna()

print("\nREGISTROS CON IMPORTE NEGATIVO")
print(
    df.loc[
        negative_amount,
        ["customer_id", "full_name", "total_spend"],
    ]
)

quarantine_mask = quality_issues.ne("")


print("\nRESUMEN DE CLASIFICACION")
print(f"Registros validos: {(~quarantine_mask).sum()}")
print(f"Registros en cuarentena: {quarantine_mask.sum()}")

quarantine_df = df.loc[quarantine_mask].copy()
clean_df = df.loc[~quarantine_mask].copy()


clean_df["full_name"] = (
    clean_df["full_name"]
    .str.strip()
    .str.title()
)

clean_df["email"] = (
    clean_df["email"]
    .str.strip()
    .str.lower()
)

clean_df["country"] = (
    clean_df["country"]
    .str.strip()
    .str.lower()
    .replace(
        {
            "es": "spain",
            "espana": "spain",
        }
    )
    .str.title()
)

clean_df["signup_date"] = (
    parsed_dates.loc[~quarantine_mask]
    .dt.strftime("%Y-%m-%d")
)

clean_df["total_spend"] = parsed_amounts.loc[~quarantine_mask]

print("\nDATOS VALIDOS")
print(clean_df)


CLEAN_PATH = Path("data/clean/customers_clean.csv")
QUARANTINE_PATH = Path("data/quarantine/customers_quarantine.csv")


quarantine_df["quality_issues"] = (
    quality_issues.loc[quarantine_mask]
    .str.rstrip("|")
)

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
