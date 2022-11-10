FROM hareendranvr/spark-base

WORKDIR /home
# -- Runtime
RUN apt-get install -y pip &&\
    apt-get install -y python3 && \
RUN pip install pyspark
ARG spark_master_web_ui=8080
COPY connect.py ./
EXPOSE ${spark_master_web_ui} ${SPARK_MASTER_PORT}
CMD ["python","./connect.py"]
