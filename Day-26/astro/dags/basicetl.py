from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
 
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}
 
dag = DAG(
    dag_id="simple_etl_in_memory",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    description="Simple ETL pipeline with in-memory data",
)
 
def extract_data(**kwargs):
    data = {
        "product": ["apple", "banana", "orange", "apple"],
        "quantity": [10, 20, 15, 5],
        "price": [2.5, 1.0, 1.5, 2.5],
    }
    df = pd.DataFrame(data)
    kwargs['ti'].xcom_push(key='raw_data', value=df.to_dict())
 
def transform_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='raw_data', task_ids='extract_task')
    df = pd.DataFrame.from_dict(data)
    df['total'] = df['quantity'] * df['price']
    df_grouped = df.groupby('product', as_index=False)['total'].sum()
    kwargs['ti'].xcom_push(key='transformed_data', value=df_grouped.to_dict())
 
def load_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='transformed_data', task_ids='transform_task')
    df = pd.DataFrame.from_dict(data)
    print("Loaded Data:\n", df)
 
extract_task = PythonOperator(
    task_id="extract_task",
    python_callable=extract_data,
    dag=dag,
)
 
transform_task = PythonOperator(
    task_id="transform_task",
    python_callable=transform_data,
    dag=dag,
)
 
load_task = PythonOperator(
    task_id="load_task",
    python_callable=load_data,
    dag=dag,
)
 
extract_task >> transform_task >> load_task