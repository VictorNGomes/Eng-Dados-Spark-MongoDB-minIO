import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import os

STORAGE = os.environ.get("AIRFLOW_DATA_PATH", "/usr/local/spark/applications")
DIRECTORY_PATH_RAW= os.path.join(STORAGE, "raw")
FILENAME = f'data_2023_7_2.json'
SOURCE_FILE = f'{DIRECTORY_PATH_RAW}/{FILENAME}'

spark = SparkSession.builder.appName("nyt_articles").getOrCreate()

df = spark.read.format("json").option("inferSchema","true").load(SOURCE_FILE)
df.printSchema()

