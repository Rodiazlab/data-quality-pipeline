import os
from dotenv import load_dotenv
import mysql.connector

def connect_to_database():
    load_dotenv()
    connection = mysql.connector.connect(
      host = os.environ["DB_HOST"],
      user = os.environ["DB_USER"],
      password = os.environ["DB_PASSWORD"],
      database = os.environ["DB_NAME"],
      port = int(os.environ["DB_PORT"])
    )

    return connection
                 

def save_customers(connection, clean_df):
    query = """
    INSERT INTO customers (
        customer_id, full_name, email, country, signup_date, total_spend
    )
    VALUES (%s, %s, %s, %s, %s, %s) As new
    ON DUPLICATE KEY UPDATE
        full_name = new.full_name,
        email = new.email,
        country = new.country,
        signup_date = new.signup_date,
        total_spend = new.total_spend
    """ 
    columns = [
        "customer_id",
        "full_name",
        "email",
        "country",
        "signup_date",
        "total_spend"
    ]
    ordered_df = clean_df[columns]
    ordered_df = ordered_df.astype(object).where(ordered_df.notna(), None)
    rows = list(ordered_df.itertuples(index=False, name=None))

    if not rows:
        return

    cursor = connection.cursor()

    try:
        cursor.executemany(query, rows)
        connection.commit()
    except mysql.connector.Error:
        connection.rollback()
        raise
    finally:
        cursor.close()

        