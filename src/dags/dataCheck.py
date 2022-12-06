import sys
sys.path.append("C:/Users/A.M. MUKTAR/Used-Car-ML/src/ivalidator")
import pandas as pd
from datetime import datetime
import logging
from datetime import datetime
from datetime import timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import random
import os
from pathlib import Path
from ivalidate import check_quality, sendAlert
import requests
from io import BytesIO  


# assign director
directory = '/c/Users/A.M. MUKTAR/Used-Car-ML/data/Passed'



#############    Fetch files from folder_A  ####################

@dag(
    dag_id='ingest_data',
    description='Ingest data from a file to another DAG',
    tags=['data_ingestion'],
    schedule=timedelta(minutes=5),
    start_date=days_ago(n=0, hour=1)
)

def ingest_data():
    ############   DATA VALIDATION JOB   ##################
    @task()
    def quality_check():
        check = check_quality()
        print(check)
        return check


    ###############  EMAIL ISSUE   #####################
    @task
    def report_issues(prob_list):
        sendAlert(prob_list)
 

    #################  INGESTION JOB  ####################
    @task
    def get_data_to_ingest_from_local_file(link) -> pd.DataFrame:
        files = list(Path(directory).glob('*.csv'))
        file = random.sample(files, 1)
        input_data_df = pd.read_csv(file[0])
        logging.info(f'Extract data from the file {directory}')
        data_to_ingest_df = input_data_df
        os.remove(file[0])
        return data_to_ingest_df

    ##########   SAVE JOB      ###########################
    @task
    def save_data(data_to_ingest_df: pd.DataFrame) -> None:
        filepath = f'/c/Users/A.M. MUKTAR/Used-Car-ML/data/output_data/{datetime.now().strftime("%Y-%M-%d_%H-%M-%S")}.csv'
        logging.info(f'Ingesting data in {filepath}')
        data_to_ingest_df.to_csv(filepath, index=False)
        logging.info(type(data_to_ingest_df))
        return data_to_ingest_df
    
    ##########  PREDICTION JOB   ###########################
    @task
    def predict_api(df: pd.DataFrame):
        file = df.drop('currentPrice', axis=1)
        data = BytesIO(file.to_csv(index=False).encode('utf-8'))
        byte_data = data.getvalue()
        response = requests.post("http://127.0.0.1:8000/file", files={"file": byte_data})
        print(response.status_code)

    ###############   Task relationships  ##################
    evaluate = report_issues(quality_check())
    data_to_ingest = get_data_to_ingest_from_local_file(evaluate)
    predict_api(save_data(data_to_ingest))
   

ingest_data_dag = ingest_data()