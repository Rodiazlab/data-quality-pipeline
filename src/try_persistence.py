import pandas as pd

from src.persistence import connect_to_database,save_customers

clean_df = pd.DataFrame(
    {
        "customer_id": ["TEST001"],
        "full_name": ["Cliente_prueba"],
        "email": ["prueba@example.com"],
        "country": ["Spain"],
        "signup_date": ["2026-09-24"],
        "total_spend": [150.00]
    }
)

connection = connect_to_database()

try:
    save_customers(connection, clean_df)
finally:
    connection.close()