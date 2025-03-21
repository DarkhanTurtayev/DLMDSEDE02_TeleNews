FROM bitnami/spark:latest

#installing python + dependencies inside container
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install pyspark nltk

RUN apt-get update && apt-get install -y netcat-openbsd


RUN apt-get update && apt-get install -y wget

RUN mkdir -p /opt/spark/jars && \
    wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.5/spark-sql-kafka-0-10_2.12-3.5.5.jar && \
    wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.1/kafka-clients-3.4.1.jar

# script
COPY spark_trends.py /opt/spark/spark_trends.py
COPY entrypoint.sh /opt/spark/entrypoint.sh

USER root
RUN chmod 755 /opt/spark/entrypoint.sh


ENTRYPOINT ["bash", "/opt/spark/entrypoint.sh"]