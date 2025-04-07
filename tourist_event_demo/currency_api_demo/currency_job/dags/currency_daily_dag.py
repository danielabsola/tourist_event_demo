from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
src_path = os.path.join(project_root, 'src')
sys.path.append(src_path)
sys.path.append(project_root)

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
    'currency_daily_update',
    default_args=default_args,
    description='Daily currency exchange rate update',
    schedule=f'0 {EXECUTION_HOUR.split(":")[0]} * * *'
)

currency_daily_etl_task = PythonOperator(
    task_id='currency_daily_etl',
    python_callable=main,
    op_kwargs={
        'is_historical': False,
        'start_date': None,  # Not needed for daily
        'end_date': None     # Not needed for daily
    },
    dag=dag
)