FROM hareendranvr/cluster-base

# -- Layer: Apache Spark

ARG spark_version=3.2.0
ARG hadoop_version=3.2

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${spark_version}-bin-hadoop${hadoop_version} /usr/bin/ && \
    mkdir /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/logs && \
    rm spark.tgz

ENV SPARK_HOME /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_PORT 7077
ENV SPARK_WORKER_PORT 8088
ENV PYSPARK_PYTHON python3
ENV SPARK_WORKER_MEMORY 2g
ENV SPARK_DRIVER_MEMORY 2g
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_WORKER_CORES 2


# -- Runtime

WORKDIR ${SPARK_HOME}