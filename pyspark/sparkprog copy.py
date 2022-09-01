### sparkprog.py
# https://stackoverflow.com/a/70269614
# run as: `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 sparkprog.py`
#######

# https://www.rittmanmead.com/blog/2017/01/getting-started-with-spark-streaming-with-python-and-kafka/
from pyspark import SparkContext
#from pyspark.streaming import StreamingContext
#from pyspark.streaming.kafka import KafkaUtils
#import json
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.functions import *

# https://sparkbyexamples.com/pyspark/pyspark-what-is-sparksession/


conf = SparkConf()
conf.setMaster("local").setAppName("ES Test")
conf.set("es.index.auto.create", "true")
conf.set("es.nodes", "log-analytics")  # name of my docker container, you might keep localhost
conf.set("es.port", "9200")

sc = SparkContext(conf=conf)

spark = SparkSession(sc)
# spark = SparkSession.builder.master("local") \
#     .appName('httpd_access_log_agg') \
#     .getOrCreate()
# sc = spark.sparkContext
# sc.setLogLevel('WARN')

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("subscribe", "httpd_access_log") \
  .load()

# https://stackoverflow.com/a/41492614
# https://www.databricks.com/blog/2017/05/08/event-time-aggregation-watermarking-apache-sparks-structured-streaming.html
df.selectExpr("timestamp", "CAST(value AS STRING)") \
  .withColumn('resp_code', regexp_extract(col('value'), 'HTTP/1.1" (\d{3})', 1)) \
  .withWatermark("timestamp", "1 minute") \
  .groupBy(window('timestamp', '1 minute'), 'resp_code') \
  .count().writeStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9092") \
  .option("topic", "log_aggregate") \
  .option("checkpointLocation", "/tmp/") \
  .start().awaitTermination() \
  

  # .format('org.elasticsearch.spark.sql') \
  # .option("checkpointLocation", "/tmp/") \
  # .option("es.resource", "index/type") \
  # .option("es.nodes", "log-analytics:9200") \
  
