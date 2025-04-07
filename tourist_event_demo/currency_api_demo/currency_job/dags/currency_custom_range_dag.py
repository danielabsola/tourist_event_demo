from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from src.main import main

EXECUTION_HOUR = os.getenv('EXECUTION_HOUR', '00:00')  # Default to midnight if not set

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'currency_custom_range_update',
    default_args=default_args,
    description='Custom currency exchange rate update',
    schedule=None
)

currency_custom_range_etl_task = PythonOperator(
    task_id='currency_custom_range_etl',
    python_callable=main,
    op_kwargs={
        'is_historical': True,
        'start_date': '{{ dag_run.conf["start_date"] }}',
        'end_date': '{{ dag_run.conf["end_date"] }}'
    },
    dag=dag
)