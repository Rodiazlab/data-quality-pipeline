import pandas as pd


def find_missing_values(
    dataframe: pd.DataFrame,
    column_name: str,
) -> pd.Series:
    return dataframe[column_name].isna()

def find_duplicates(
    dataframe: pd.DataFrame,
    column_name: str,
) -> pd.Series:
    return dataframe[column_name].duplicated(keep=False)
