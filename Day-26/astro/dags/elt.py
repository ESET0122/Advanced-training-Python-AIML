from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd
import psycopg2

POSTGRES_CONN = {
    "host": "postgres",  # matches docker service
    "database": "airflow",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}

@dag(
    dag_id="elt_postgres_dag",
    start_date=datetime(2025, 11, 12),
    schedule=None,
    catchup=False,
    tags=["elt", "postgres"]
)
def elt_postgres_dag():
    @task
    def extract():
        # Replace with your source; here, we'll simulate
        data = [
            {"id": 1, "value": 100},
            {"id": 2, "value": 200}
        ]
        return data

    @task
    def transform(data):
        df = pd.DataFrame(data)
        df["value_squared"] = df["value"] ** 2
        return df.to_dict(orient="records")

    @task
    def load_to_postgres(records):
        df = pd.DataFrame(records)
        conn = psycopg2.connect(**POSTGRES_CONN)
        cur = conn.cursor()
        # Create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS elt_table (
                id INT PRIMARY KEY,
                value INT,
                value_squared INT
            )
        """)
        # Upsert data
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO elt_table (id, value, value_squared)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                  value = EXCLUDED.value,
                  value_squared = EXCLUDED.value_squared
                """,
                (int(row["id"]), int(row["value"]), int(row["value_squared"]))
            )
        conn.commit()
        cur.close()
        conn.close()

    load_to_postgres(transform(extract()))

elt_postgres_dag()
