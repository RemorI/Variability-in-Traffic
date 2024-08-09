from datetime import datetime
import json
import requests

from airflow import DAG
from airflow.operators.python import PythonOperator

from api_keys import API_Weather, API_Traffic

default_args = {
    'owner': 'blight',
    'start_date': datetime(2024, 8, 8, 00, 00),
    'schedule_interval': '@daily',
}

def call_weather():
    lat = ''
    lon = ''
    API_key = API_Weather
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'

def call_traffic():
    x=1

with DAG (
    'traffic-climate-analysis',
    catchup = False,
) as dag:
    streaming_task = PythonOperator(
        task_id = 'stream-weather',
        python_callable = call_weather
    )