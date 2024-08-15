from datetime import datetime
import json
import requests
import pandas as pd

#from airflow import DAG
#from airflow.operators.python import PythonOperator

from api_keys import API_Weather, API_Traffic

# default_args = {
#     'owner': 'blight',
#     'start_date': datetime(2024, 8, 8, 00, 00),
#     'schedule_interval': '@daily',
# }

def call_weather():
    lat = ''
    lon = ''
    API_key = API_Weather
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'

def extract_traffic():
    url = 'https://eismoinfo.lt/traffic-intensity-service#'
    res = requests.get(url)
    res = res.json()

    return res

def transform_traffic(res):
    df = pd.json_normalize(res, 'roadSegments', ['id', 'name', 'roadNr', 'roadName', 'km', 'x', 'y'])
    df = df[['id', 'name', 'roadNr', 'roadName', 'km', 'x', 'y', 'direction', 'numberOfVehicles', 'averageSpeed', 'trafficType', 'winterSpeed', 'summerSpeed']]
    
    return df

def load_traffic():
    res = extract_traffic()
    df = transform_traffic(res)
    print(df)



# with DAG (
#     'traffic-climate-analysis',
#     catchup = False,
# ) as dag:
#     streaming_task = PythonOperator(
#         task_id = 'stream-traffic',
#         python_callable = extract_traffic
#     )

load_traffic()