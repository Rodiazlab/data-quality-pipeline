import pandas as pd

from src.pipeline import process_customers

def test_process_customers_splits_clean_and_quarantine_dataframes():
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002", "C003"],
            "full_name": [" Ana López ", "Luis Pérez", "María Gómez"],
            "email": ["ANA@EXAMPLE.COM", "luis@example.com", "maria@example.com"],
            "signup_date": ["2026-01-15", "15/02/2026", "31/02/2026"],
            "total_spend": ["1250.50", "890,40", "not_available"],
            "country": ["ES", "espana", "france"],
        }
    )

    clean_df, quarantine_df = process_customers(dataframe)
    assert clean_df.shape[0] == 2
    assert quarantine_df.shape[0] == 1
    assert clean_df["customer_id"].to_list() == ["C001", "C002"]
    assert quarantine_df["customer_id"].to_list() == ["C003"]
    assert clean_df["email"].to_list() == ["ana@example.com", "luis@example.com"]
    assert clean_df["full_name"].to_list() == ["Ana López", "Luis Pérez"]
    assert clean_df["country"].to_list() == ["Spain", "Spain"]  
    assert clean_df["signup_date"].to_list() == ["2026-01-15", "2026-02-15"]
    assert clean_df["total_spend"].to_list() == [1250.50, 890.40]   
    assert quarantine_df["quality_issues"].to_list() == ["INVALID_SIGNUP_DATE|INVALID_AMOUNT"]