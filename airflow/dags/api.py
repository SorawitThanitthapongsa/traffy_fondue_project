from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime
from airflow.utils.dates import days_ago
from datetime import timedelta

import pandas as pd
from datetime import datetime, timezone
import os
import json
import requests
import time

def get_data_from_request():
    if os.path.exists('/opt/airflow/dags/data/fondue-data.csv') == False:
        f = open("/opt/airflow/dags/data/fondue-data.csv", "x")

    url = 'https://publicapi.traffy.in.th/dump-csv-chadchart/bangkok_traffy.csv'
    output_file = '/opt/airflow/dags/data/fondue-data.csv'

    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check for any error status

    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def clean_data():
    
    path = "/opt/airflow/dags/data/fondue-data.csv"
    df = pd.read_csv(path)

    df_type = df[df["state"] == "เสร็จสิ้น"]
    bangkok = ["กรุงเทพมหานคร","จังหวัดกรุงเทพมหานคร","จังหวัดจังหวัด กรุงเทพมหานคร","จังหวัดBangkok","จังหวัดจังหวัดกรุงเทพมหานคร"]
    df_type_pro = df_type[df_type["province"].isin(bangkok)]

    df_type_pro["timestamp"]=pd.to_datetime(df_type_pro["timestamp"])

    df_type_pro["last_activity"] = pd.to_datetime(df_type_pro["last_activity"])
    df_type_pro["duration"] = df_type_pro["last_activity"]-df_type_pro["timestamp"]

    df_type_pro = df_type_pro[df_type_pro["district"].isnull() == False]
    df_type_pro = df_type_pro[df_type_pro["type"].isnull() == False]
    df_type_pro = df_type_pro[df_type_pro["type"] != "{}"]

    df_type_pro_dpro = df_type_pro.drop(columns=["province","state","photo","photo_after"])
    df_type_pro_dpro['type'] = [x[1:-1] for x in df_type_pro_dpro['type']]
    df_type_pro_dpro['type']= df_type_pro_dpro['type'].str.split(",", n = 1, expand = False)
    type_df = df_type_pro_dpro[df_type_pro_dpro.type.apply(lambda x: len(x)) == 1]

    df_feature = df_type_pro_dpro[['type', 'district','timestamp','duration']]

    df_feature['duration'] = pd.to_timedelta(df_feature['duration'])
    df_feature['duration'] = df_feature['duration'] / pd.Timedelta(hours=1)
    df_feature.rename(columns={'duration': 'duration_hour'}, inplace=True)

    df_feature.to_csv("/opt/airflow/dags/data/cleaned_data.csv")



with DAG(
    dag_id='traffy_fetch_data',
    schedule_interval='@daily',
    start_date=datetime(2023, 5, 15),
    catchup=False,
    tags=["datasci"],
) as dag:
    fetchData = PythonOperator(
        task_id='fetch_data',
        python_callable=get_data_from_request
    )
    
    cleanData = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data
    )
    
    fetchData >> cleanData