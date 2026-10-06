import pandas as pd
from src.metrics import (calculate_quality_metrics,
                         count_quality_issues,
                         build_quality_summary,
                         save_quality_summary
)  

import json


def test_calculate_quality_metrics_counts_records():
    df =pd.DataFrame({"customer_id": ["C001", "C002", "C003", "C004", "C005"]})
    clean_df = pd.DataFrame({"customer_id": ["C001", "C002", "C003"]})
    quarantine_df = pd.DataFrame({"customer_id": ["C004", "C005"]})
    result = calculate_quality_metrics(df, clean_df, quarantine_df)
    
    assert result == {
        "received_records": 5,
        "valid_records": 3,
        "quarantine_records": 2,
        "valid_percentage": 60.0,
        "quarantine_percentage": 40.0,
    }

def test_calculate_quality_metrics_handles_empty_batch():
    df = pd.DataFrame({"customer_id": []})
    clean_df = pd.DataFrame({"customer_id": []})
    quarantine_df = pd.DataFrame({"customer_id": []})
    result = calculate_quality_metrics(df, clean_df, quarantine_df)
    
    assert result == {
        "received_records": 0,
        "valid_records": 0,
        "quarantine_records": 0,
        "valid_percentage": 0.0,
        "quarantine_percentage": 0.0,
    }

def test_count_quality_issues_counts_each_reason():
    quarantine_df = pd.DataFrame({
        "quality_issues": [
            "INVALID_EMAIL",
            "INVALID_SIGNUP_DATE|NEGATIVE_AMOUNT",
            "INVALID_EMAIL",
        ]
    })
    result = count_quality_issues(quarantine_df)

    assert result == {
        "INVALID_EMAIL": 2,
        "INVALID_SIGNUP_DATE": 1,
        "NEGATIVE_AMOUNT": 1
    }       

def test_count_quality_issues_handles_empty_quarantine():
    quarantine_df = pd.DataFrame({
        "quality_issues": pd.Series(dtype="string")
    })

    result = count_quality_issues(quarantine_df)
    assert result == {}

def test_build_quality_summary_combines_metrics_and_issues():
    df = pd.DataFrame({"customer_id": ["C001", "C002", "C003", "C004", "C005"]})
    clean_df = pd.DataFrame({"customer_id": ["C001", "C002", "C003"]})
    quarantine_df = pd.DataFrame({
        "customer_id": ["C004", "C005"],
        "quality_issues": [
             "INVALID_EMAIL",
             "INVALID_SIGNUP_DATE|NEGATIVE_AMOUNT"
        ]
    })

    result = build_quality_summary(df, clean_df, quarantine_df)

    assert result == {
        "received_records": 5,
        "valid_records": 3,
        "quarantine_records": 2,
        "valid_percentage": 60.0,
        "quarantine_percentage": 40.0,
        "quality_issues": {
             "INVALID_EMAIL": 1,
             "INVALID_SIGNUP_DATE": 1,
             "NEGATIVE_AMOUNT": 1
        }
    }   

def test_save_quality_summary_writes_json(tmp_path):
    summary = {
        "received_records": 3,
        "quality_issues": {"INVALID_EMAIL": 1},
    }
    output_path = tmp_path / "summary.json"

    save_quality_summary(summary, output_path)
    with open(output_path, "r", encoding="utf-8") as file:
        saved_summary = json.load(file)

    assert saved_summary == summary