from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace, count, to_timestamp, max as spark_max, window
import sys
import nltk
from nltk.corpus import stopwords

# ignore words (a, the, for, it etc.)
nltk.download('stopwords')
ignore = set(stopwords.words('english'))

# Spark session
spark = SparkSession.builder.appName("GlobalTrends").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("\n SUCCESS: Spark is working \n")

# Kafka connection
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "telenews-kafka-1:9092").option("subscribe", "telegram_news")\
    .option("startingOffsets", "earliest").load() \
    .selectExpr("CAST(value AS STRING) AS message", "timestamp")
df = df.withColumn("timestamp", to_timestamp(col("timestamp"))) 

# messages normalization + links filtration
words = df.select(explode(split(lower(regexp_replace(col("message"), r'(https?://\S+|href="[^"]*"|/b|/b|\*\*|[^a-zA-Z\s])', '')),"\s+")).alias("word"),
                  col("timestamp")).filter(~col("word").isin(ignore))

# main logic (sort words frequency)
trends = words.withWatermark("timestamp", "30 minutes").groupBy("word").agg(count("word").alias("count"), spark_max("timestamp").alias("last_timestamp")).orderBy(col("count").desc())
activity = df.select(col("message"), col("timestamp"))


# aggregated trends to Kafka (topic: trending_words), frequent content, additional streamline if needed to push forward
query_kafka = trends.selectExpr("CAST(word AS STRING) AS key", "CAST(count AS STRING) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "telenews-kafka-1:9092") \
    .option("topic", "trending_words") \
    .outputMode("complete") \
    .option("checkpointLocation", "/tmp/checkpoints_kafka") \
    .trigger(processingTime="30 seconds") \
    .start()

# logs
query_console = trends.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="30 seconds") \
    .start()

# to db 
query_postgres_trends = trends.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch: df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/spark_db") \
        .option("dbtable", "public.word_counts") \
        .option("user", "admin") \
        .option("password", "admin") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()) \
    .trigger(processingTime="30 seconds") \
    .start()

query_postgres_activity = activity.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch: df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/spark_db") \
        .option("dbtable", "public.activity") \
        .option("user", "admin") \
        .option("password", "admin") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()) \
    .trigger(processingTime="30 seconds") \
    .start()

query_kafka.awaitTermination()
query_console.awaitTermination()
query_postgres_trends.awaitTermination()
query_postgres_activity.awaitTermination()