import pandas as pd

from src.classification import classify_records

from src.cleaning import (
     normalize_amounts,
     parse_mixed_dates,
)

def process_customers(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    
    parsed_dates = parse_mixed_dates(
        dataframe,
        "signup_date",
    )

    parsed_amounts = normalize_amounts(
        dataframe,
        "total_spend",
    )

    quality_issues = classify_records(
        dataframe,
        parsed_dates,
        parsed_amounts,
    )   

    quarantine_mask = quality_issues.ne("")
    quarantine_df = dataframe.loc[quarantine_mask].copy()
    clean_df = dataframe.loc[~quarantine_mask].copy()

    quarantine_df["quality_issues"] = quality_issues.loc[quarantine_mask]

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

    return clean_df, quarantine_df



