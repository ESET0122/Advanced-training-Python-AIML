
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import get_current_context
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2

with DAG(
    dag_id="sample_elt_dag",
    description="A simple ELT pipeline example",
    start_date=datetime(2025, 11, 11),
    schedule="*/2 * * * *",   # corrected parameter name
    catchup=False,
    tags=["example", "elt", "training"],
) as dag:

    def extract_data():
        data = pd.read_csv("iris.csv")
        print("✅ Extracted data:", data.head())
        return data.to_dict(orient="records")

   
    def load_data():
        context = get_current_context()
        extracted_data = context["ti"].xcom_pull(task_ids="extract_task")
        df = pd.DataFrame(extracted_data)

        db_user = "postgres"
        db_pass = "postgres"
        db_host = "postgres"
        db_port = "5432"
        db_name = "airflow"

       
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_pass,
                host=db_host,
                port=db_port,
            )
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = cur.fetchone()
            if not exists:
                cur.execute(f'CREATE DATABASE "{db_name}"')
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
            cur.close()
            conn.close()
        except Exception as e:
            print("Error while checking/creating database:", e)
            raise

        engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
        df.to_sql(name="iris_data", con=engine, if_exists="append", index=False)
       

        return df.to_dict(orient="records")

    def transform_data():
        context = get_current_context()
        data = context["ti"].xcom_pull(task_ids="load_task")
        df = pd.DataFrame(data)

  
        df.columns = [col.upper() for col in df.columns]
        print("✅ Transformed data (first 5 rows):")
        print(df.head())

        return df.to_dict(orient="records")


    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract_data,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_data,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform_data,
    )

    # Task flow
    extract_task >> load_task >> transform_task

 