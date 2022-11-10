FROM hareendranvr/spark-base

# -- Runtime

ARG spark_worker_web_ui=8081

EXPOSE ${spark_worker_web_ui} ${SPARK_WORKER_PORT}
RUN echo ${SPARK_MASTER_HOST}
CMD bin/spark-class org.apache.spark.deploy.worker.Worker spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT} >> logs/spark-worker.out
# CMD bash sbin/start-worker.sh spark://{SPARK_MASTER_HOST}:{SPARK_MASTER_PORT} >> logs/spark-worker.out