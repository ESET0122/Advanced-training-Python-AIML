from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

# DAG definition
dag = DAG(
    "kaggle_elt_pandas",
    default_args={"owner": "airflow", "start_date": datetime(2025, 11, 11)},
    schedule="@daily",
    catchup=False
)

DATA_DIR = "C:/Users/HP/Desktop/Advanced-trainin-Python-AIML/Day-26/Apache_Airflow/Data_start"

# Ensure the folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Extract Task
def extract_data():
    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "score": [5, 15, 8, 20]
    })
    df.to_csv(os.path.join(DATA_DIR, "raw_data.csv"), index=False)
    print("✅ raw_data.csv saved")

# Load Task (store raw data somewhere)
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "raw_data.csv"))
    df.to_csv(os.path.join(DATA_DIR, "loaded_data.csv"), index=False)
    print("✅ loaded_data.csv saved\n", df.head())

# Transform Task (operate on loaded data)
def transform_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "loaded_data.csv"))
    df_filtered = df[df["score"] > 10]
    df_filtered.to_csv(os.path.join(DATA_DIR, "transformed_data.csv"), index=False)
    print("✅ transformed_data.csv saved\n", df_filtered.head())

# Airflow tasks
extract = PythonOperator(task_id="extract", python_callable=extract_data, dag=dag)
load = PythonOperator(task_id="load", python_callable=load_data, dag=dag)
transform = PythonOperator(task_id="transform", python_callable=transform_data, dag=dag)

# ELT order: Extract -> Load -> Transform
extract >> load >> transform
