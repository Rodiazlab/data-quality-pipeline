import pandas as pd

from src.validation import (
    find_duplicates,
    find_missing_values
)

def classify_records(
    dataframe: pd.DataFrame,
    parsed_dates: pd.Series,
    parsed_amounts: pd.Series,
) -> pd.Series:
    
    quality_issues = pd.Series(
        "",
        index=dataframe.index,
        dtype="string",
    )

    missing_customer_id = find_missing_values(
        dataframe,
        "customer_id",
    )
    quality_issues.loc[missing_customer_id] = (
        quality_issues.loc[missing_customer_id]
        + "MISSING_CUSTOMER_ID|"
    )

    missing_email = find_missing_values(
        dataframe,
        "email",
    )
    quality_issues.loc[missing_email] = (
        quality_issues.loc[missing_email]
        + "MISSING_EMAIL|"
    )
    duplicate_customer_id = find_duplicates(
        dataframe,
        "customer_id",
    )
    quality_issues.loc[duplicate_customer_id] = (
        quality_issues.loc[duplicate_customer_id]
        + "DUPLICATED_CUSTOMER_ID|"
    )
    return quality_issues.str.rstrip("|")

