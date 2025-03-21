#!/bin/bash


echo "Waiting for Kafka on port 9092..."
while ! nc -z kafka 9092; do
  sleep 1
done
echo "Kafka is available!"

if [ "$SPARK_MODE" == "master" ]; then
    echo "Starting Spark Master"
    /opt/bitnami/spark/bin/spark-class org.apache.spark.deploy.master.Master --host 0.0.0.0 &
    

    sleep 10
    
    echo "Launching spark_trends.py "
    /opt/bitnami/spark/bin/spark-submit \
        --master spark://spark-master:7077 \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,org.postgresql:postgresql:42.7.3 \
        /opt/spark/spark_trends.py
elif [ "$SPARK_MODE" == "worker" ]; then
    echo " Starting Spark Worker"
    /opt/bitnami/spark/bin/spark-class org.apache.spark.deploy.worker.Worker "$SPARK_MASTER_URL"
else
    echo " Check mode "
    exit 1
fi