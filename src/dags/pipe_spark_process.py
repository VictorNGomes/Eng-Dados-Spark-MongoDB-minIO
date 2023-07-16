import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
import requests
import json

spark_conn = os.environ.get("spark_conn", "spark_conn")
spark_master = "spark://spark:7077"
spark_app_name = "news"
now = datetime.now()

S3_RAW = 'raw'
S3_CONN ='minio_conn'

API_KEY = 'eVpSbJPpvnWzw02eB8kv0ra3tX59cuhI'
API_URL = f'https://api.nytimes.com/svc/archive/v1/{now.year}/{now.month}.json'


STORAGE = os.environ.get("AIRFLOW_DATA_PATH", "/usr/local/spark/applications")
DIRECTORY_PATH_RAW= os.path.join(STORAGE, "raw")
FILENAME = f'data_{now.year}_{now.month}.json'

SOURCE_FILE = f'{DIRECTORY_PATH_RAW}/{FILENAME}'

def get_data_from_API():
    params = {
        'api-key': API_KEY
    }
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data['response']['docs']

        return articles
    else:
        print('Error occurred while fetching articles:', response.text)

def save_local_storage(bucket,data):
    if bucket == S3_RAW:
        if not os.path.exists(DIRECTORY_PATH_RAW):
            os.makedirs(DIRECTORY_PATH_RAW)
            print(f"Directory '{DIRECTORY_PATH_RAW}' created.")

        else:
            print(f"Directory '{DIRECTORY_PATH_RAW}' already exists.")   

        with open(os.path.join(DIRECTORY_PATH_RAW,FILENAME), "w") as file:
            json.dump(data, file)
            print(f"JSON data saved to {FILENAME}") 

def get_from_API_and_storage_local_on(**kwargs):
    data = get_data_from_API()
    save_local_storage(bucket=kwargs.get("bucket"),data=data)

def upload_file(**kwargs) -> None:
    s3_conn = kwargs.get("s3_conn")
    bucket = kwargs.get("bucket")
    source_filename = kwargs.get("source_filename")    
    dest_filename = FILENAME

    s3 = S3Hook(s3_conn)
    s3.load_file(source_filename,
                 key=dest_filename,
                 bucket_name=bucket,
                 replace = True)




default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    start_date = datetime(2023,7,5),
    dag_id="nyt_articles_process",
    description="This DAG runs a simple pipeline for gets news and put datalake and bd.",
    default_args=default_args,
    schedule_interval=timedelta(1)
)

start = DummyOperator(task_id="start", dag=dag)

get_nyt_article_from_url_and_storage = PythonOperator(
        task_id='get_nyt_article_from_API',
        python_callable=get_from_API_and_storage_local_on,
        provide_context=True,
        op_kwargs={
            'bucket': S3_RAW,    
        }
        
    )

upload_file_to_s3 = PythonOperator(
        task_id='upload_nyt_articles_to_s3',
        provide_context=True,
        python_callable=upload_file,
        op_kwargs={
            'source_filename': SOURCE_FILE,
            'bucket': S3_RAW,
            's3_conn': S3_CONN
        }
    )

spark_job = SparkSubmitOperator(
    task_id="spark_filter_to_mongodb",
    # Spark application path created in airflow and spark cluster
    application="/usr/local/spark/applications/spark_and_minio.py",
    name=spark_app_name,
    conn_id=spark_conn,
    verbose=1,
    conf={"spark.master": spark_master},
    # application_args=[file_path],
    dag=dag)

end = DummyOperator(task_id="end", dag=dag)

start >> get_nyt_article_from_url_and_storage >>[ upload_file_to_s3, spark_job] >> end