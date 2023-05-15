from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
import os
import json
import requests
import time

def get_data_from_request():
    if os.path.exists('./data/current.csv') == False:
        f = open("/opt/airflow/dags/data/fondue-data.csv", "x")

    url = 'https://publicapi.traffy.in.th/dump-csv-chadchart/bangkok_traffy.csv'
    output_file = '/opt/airflow/dags/data/fondue-data.csv'

    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check for any error status

    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

with DAG(
    dag_id='traffy_fetch_data',
    schedule_interval='@daily',
    start_date=datetime(2023, 5, 15),
    catchup=False,
    tags=["datasci"],
) as dag:
    fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=get_data_from_request
    )