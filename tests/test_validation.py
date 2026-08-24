import pandas as pd

from src.validation import (
    find_duplicates,
    find_missing_values,
)


def test_find_missing_values_detects_empty_customer_id():
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", None, "C003"],
        }
    )

    result = find_missing_values(
        dataframe,
        "customer_id",
    )

    assert result.tolist() == [False, True, False]

def test_find_duplicates_marks_all_repeated_values():
    dataframe = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C002",
                "C002",
                "C003",
            ],
        }
    )

    result = find_duplicates(
        dataframe,
        "customer_id",
    )

    assert result.tolist() == [
        False,
        True,
        True,
        False,
    ]
