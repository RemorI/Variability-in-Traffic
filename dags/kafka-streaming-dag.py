from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'blight',
    'start_date': datetime(2024, 08, 08, 00, 00),
}

datetime()