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
def normalize_amounts(
    dataframe: pd.DataFrame,
    column_name: str,
) -> pd.Series:
    amount_text = dataframe[column_name].str.strip()

    uses_european_format = amount_text.str.contains(
        ",",
        regex=False,
        na=False,
    )

    normalized_text = amount_text.copy()

    normalized_text.loc[uses_european_format] = (
        amount_text.loc[uses_european_format]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    return pd.to_numeric(
        normalized_text,
        errors="coerce",
    )
