from pathlib import Path

import pandas as pd

from src.validation import (
    find_duplicates,
    find_missing_values,
)


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

invalid_email = (
    df["email"].notna()
    & ~df["email"].str.contains("@", regex=False, na=False)
)

print("\nREGISTROS CON EMAIL INVALIDO")
print(df[invalid_email])

parsed_dates = pd.to_datetime(
    df["signup_date"],
    format="mixed",
    dayfirst=True,
    errors="coerce",
)

invalid_signup_date = parsed_dates.isna()

print("\nREGISTROS CON FECHA INVALIDO")
print(df[invalid_signup_date])

amount_text = df["total_spend"].str.strip()

uses_european_format = amount_text.str.contains(
    ",",
    regex=False,
    na=False,
)

print("\nIMPORTES CON FORMATO EUROPEO")
print(df.loc[uses_european_format, ["customer_id", "total_spend"]])

normalized_amount_text = amount_text.copy()
normalized_amount_text.loc[uses_european_format] = (
    amount_text.loc[uses_european_format]
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)

parsed_amounts = pd.to_numeric(
    normalized_amount_text,
    errors="coerce",
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

quarantine_mask = (
    missing_customer_id
    | missing_email
    | duplicated_customer_id
    | invalid_email
    | invalid_signup_date
    | invalid_amount
    | negative_amount
)

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

print("\nDATOS EN CUARENTENA")
print(quarantine_df)

CLEAN_PATH = Path("data/clean/customers_clean.csv")
QUARANTINE_PATH = Path("data/quarantine/customers_quarantine.csv")

quality_rules = {
    "MISSING_CUSTOMER_ID": missing_customer_id,
    "MISSING_EMAIL": missing_email,
    "DUPLICATED_CUSTOMER_ID": duplicated_customer_id,
    "INVALID_EMAIL": invalid_email,
    "INVALID_SIGNUP_DATE": invalid_signup_date,
    "INVALID_AMOUNT": invalid_amount,
    "NEGATIVE_AMOUNT": negative_amount,
}

quality_issues = pd.Series(
    "",
    index=df.index,
    dtype="string",
)

for issue_name, condition in quality_rules.items():
    quality_issues.loc[condition] = (
        quality_issues.loc[condition]
        + issue_name
        + "|"
    )

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
