import pandas as pd

from src.cleaning import parse_mixed_dates


def test_parse_mixed_dates_converts_valid_and_invalid_values():
    dataframe = pd.DataFrame(
        {
            "signup_date": [
                "2026-01-15",
                "15/02/2026",
                "31/02/2026",
            ],
        }
    )

    result = parse_mixed_dates(
        dataframe,
        "signup_date",
    )

    assert result.iloc[0] == pd.Timestamp("2026-01-15")
    assert result.iloc[1] == pd.Timestamp("2026-02-15")
    assert pd.isna(result.iloc[2])
