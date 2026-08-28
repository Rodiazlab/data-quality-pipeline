import pandas as pd
from src.classification import classify_records

def test_classify_records_identifies_empty_customer_id():
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002", "C003", None],
            "email": ["ana@example.com",
                     "luis@example.com",
                     "maria@example.com",
                     "joao@example.com"]

        }
    )
    parsed_dates = pd.Series(
        [
            "2026-01-01",
            "2026-02-01",
            "2026-03-01",
            "2026-04-01"
        ]
    )

    parsed_amounts = pd.Series(
        [
            100.0,
            200.0,
            300.0,
            400.0
        ]
    )

    result = classify_records(dataframe, parsed_dates, parsed_amounts)  
    assert result.to_list() == ["", "", "", "MISSING_CUSTOMER_ID"]
