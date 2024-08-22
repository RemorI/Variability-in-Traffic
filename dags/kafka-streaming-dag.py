from datetime import datetime
import json
import requests
import pandas as pd
from kafka import KafkaProducer

#from airflow import DAG
#from airflow.operators.python import PythonOperator

# default_args = {
#     'owner': 'blight',
#     'start_date': datetime(2024, 8, 8, 00, 00),
#     'schedule_interval': '@daily',
# }

def extract_weather():
    url = 'https://eismoinfo.lt/weather-conditions-service'
    res_w = requests.get(url)
    res_w = res_w.json()

    return res_w

def transform_weather(res_w):
    df_w = pd.json_normalize(res_w)

    df_w = df_w[['id', 'irenginys', 'numeris', 'pavadinimas', 'oro_temperatura', 'krituliu_tipas', 'krituliu_kiekis', 'uzsalimo_taskas', 'dangos_temperatura', 'kelio_danga', 'vejo_greitis_maks', 'vejo_greitis_vidut', 'vejo_kryptis', 'sukibimo_koeficientas', 'matomumas', 'kilometras', 'lat', 'lng', 'surinkimo_data']]
    df_w.columns = ['id', 'station', 'roadNr', 'roadName', 'air_temperature', 'precipitation_type', 'precipitation_amount', 'freezing_point', 'surface_temperature', 'surface_condition', 'max_wind_speed', 'avg_wind_speed', 'wind_direction', 'friction', 'visibility', 'km', 'x', 'y', 'date']
    
    replace_direction = {
        'Pietų': 'South',
        'Pietryčių': 'Southeast',
        'Pietvakarių': 'Southwest',
        'Šiaurės': 'North', 
        'Šiaurės rytų': 'Northeast',
        'Šiaurės vakarų': 'Northwest',
        'Rytų': 'East',
        'Vakarų': 'West',
    }

    replace_precipitation = {
        'Nėra': 'No rain',
        'Lietus, silpnas': 'Light rain',
        'Migla': 'Foggy',
    }

    df_w['wind_direction'] = df_w['wind_direction'].replace(replace_direction)
    df_w['precipitation_type'] = df_w['precipitation_type'].replace(replace_precipitation)
    
    return df_w


def extract_traffic():
    url = 'https://eismoinfo.lt/traffic-intensity-service#'
    res_t = requests.get(url)
    res_t = res_t.json()

    return res_t

def transform_traffic(res_t):
    df_t = pd.json_normalize(res_t, 'roadSegments', ['id', 'name', 'roadNr', 'roadName', 'km', 'x', 'y', 'date'])
    df_t = df_t[['id', 'name', 'roadNr', 'roadName', 'km', 'x', 'y', 'direction', 'numberOfVehicles', 'averageSpeed', 'trafficType', 'winterSpeed', 'summerSpeed', 'date']]
    
    return df_t

def load_traffic():
    res_t = extract_traffic()
    df_t = transform_traffic(res_t)

    res_w = extract_weather()
    df_w = transform_weather(res_w)
    
    #return df_t, df_w

    df_t = pd.DataFrame.to_json(df_t)

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    producer.send('daily_traffic', json.dumps(df_t).encode('utf-8'))

# with DAG (
#     'traffic-climate-analysis',
#     catchup = False,
# ) as dag:
#     streaming_task = PythonOperator(
#         task_id = 'stream-traffic',
#         python_callable = extract_traffic
#     )

load_traffic()
#print(Data_Traffic.iloc[0], Data_Weather.iloc[0])