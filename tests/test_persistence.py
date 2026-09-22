from unittest.mock import Mock

import pandas as pd

import pytest
import mysql.connector

from src.persistence import save_customers

def test_save_customers_empty_dataframe_does_not_use_connection():
    connection = Mock()
    cleaned_df = pd.DataFrame(columns=[
        "customer_id", 
        "full_name", 
        "email",
        "country",
        "signup_date",
        "total_spend"
    ]) 
    save_customers(connection, cleaned_df)
    connection.cursor.assert_not_called()

def test_save_customers_saves_one_customer():
    connection = Mock()
    clean_df = pd.DataFrame({
        "customer_id": ["C001"],
        "full_name": ["Ana López"],
        "email": ["ana@example.com"],
        "country": ["Spain"],
        "signup_date": ["2026-01-15"],
        "total_spend": [1250.50]
    })
    save_customers(connection, clean_df)
    connection.cursor.assert_called_once()
    connection.commit.assert_called_once()
    connection.cursor.return_value.close.assert_called_once()
    cursor = connection.cursor.return_value
    cursor.executemany.assert_called_once()
    sent_rows = cursor.executemany.call_args.args[1]

    assert sent_rows == [
       ("C001", "Ana López", "ana@example.com", "Spain", "2026-01-15", 1250.50)
    ]
def test_save_customers_rolls_back_on_error():
    connection = Mock()
    cursor = connection.cursor.return_value
    cursor.executemany.side_effect = mysql.connector.Error("Fallo simulado")
    clean_df = pd.DataFrame({
        "customer_id": ["C001"],
        "full_name": ["Ana López"],
        "email": ["ana@example.com"],
        "country": ["Spain"],
        "signup_date": ["2026-01-15"],
        "total_spend": [1250.50]
    })

    with pytest.raises(mysql.connector.Error, match="Fallo simulado"):
        save_customers(connection, clean_df)

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.cursor.return_value.close.assert_called_once()

def test_save_customers_converts_missing_values_to_none():
    connection = Mock()
    clean_df = pd.DataFrame({
        "customer_id": ["C001"],
        "full_name": [pd.NA],
        "email": ["ana@example.com"],
        "country": [pd.NA],
        "signup_date": ["2026-01-15"],
        "total_spend": [1250.50]
    })
    save_customers(connection, clean_df)
    connection.cursor.assert_called_once()
    connection.commit.assert_called_once()
    connection.cursor.return_value.close.assert_called_once()
    cursor = connection.cursor.return_value
    cursor.executemany.assert_called_once()
    sent_rows = cursor.executemany.call_args.args[1]

    assert sent_rows == [
        ("C001", None, "ana@example.com", None, "2026-01-15", 1250.50)
    ]