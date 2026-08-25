import pandas as pd


def parse_mixed_dates(
    dataframe: pd.DataFrame,
    column_name: str,
) -> pd.Series:
    return pd.to_datetime(
        dataframe[column_name],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )
