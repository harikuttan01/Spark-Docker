FROM hareendranvr/spark-base-2

# -- Runtime

ARG spark_master_web_ui=8080
ARG SPARK_MASTER_HOST=192.168.246.87

EXPOSE ${spark_master_web_ui} ${SPARK_MASTER_PORT}
CMD bin/spark-class org.apache.spark.deploy.master.Master >> logs/spark-master.out