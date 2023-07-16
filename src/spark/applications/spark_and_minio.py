import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import os
import requests
from datetime import datetime, timedelta

now = datetime.now()

os.system(
    "pip install pymongo"
)
from pymongo import MongoClient

STORAGE = os.environ.get("AIRFLOW_DATA_PATH", "/usr/local/spark/applications")
DIRECTORY_PATH_RAW= os.path.join(STORAGE, "raw")
FILENAME = f'data_{now.year}_{now.month}.json'
SOURCE_FILE = f'{DIRECTORY_PATH_RAW}/{FILENAME}'





client = MongoClient('mongodb://airflow:airflow@mongo:27017')
db = client['admin']

collection = db[f'notices_{now.year}_{now.month}']



spark = SparkSession.builder.appName("nyt_articles")\
    .config("spark.mongodb.input.uri", "mongodb://airflow:airflow/admin.notices") \
    .config("spark.mongodb.output.uri", "mongodb://airflow:airflow/admin.notices") \
    .getOrCreate()

API_KEY = 'eVpSbJPpvnWzw02eB8kv0ra3tX59cuhI'
API_URL = 'https://api.nytimes.com/svc/archive/v1/2023/7.json'


params = {
    'api-key': API_KEY
}
response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data = response.json()
    articles = data['response']['docs']

    df = spark.createDataFrame(articles)

    tech_articles = df.filter(df.section_name.contains("Technology"))
    tech_articles = tech_articles.select("headline.main", "web_url", "pub_date")
    tech_articles.show(truncate=False, n=tech_articles.count())

    articles_data = tech_articles.toPandas().to_dict('records')

    documents_to_insert = []

    for article in articles_data:
        if collection.find_one({'main': article['main']}) is None:
            documents_to_insert.append(article)

    if documents_to_insert:
        result = collection.insert_many(documents_to_insert, ordered=False)
        print(f"Successfully inserted {len(result.inserted_ids)} documents.")
    else:
        print("No new documents to insert.")



else:
    print('Error occurred while fetching articles:', response.text)


saved_data = collection.find()

for data in saved_data:
    print(data)


