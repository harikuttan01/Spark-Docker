FROM itayb/spark:3.1.1-hadoop-3.2.0-aws

WORKDIR /home

RUN mkdir -p /opt/conda/lib/python3.7/site-packages && \
    chmod 777 -R /opt/conda/lib/python3.7/site-packages && \
    ln -s python3.7 /usr/bin/python

RUN pip install \
    notebook==6.2.0 \
    ipynb==0.5.1 \
    sparkmonitor==1.1.1 \
    pyspark==3.1.1 --target=/opt/conda/lib/python3.7/site-packages \
    pip install wget
ENV PYTHONPATH=:/opt/conda/lib/python3.7/site-packages \
    PATH=$PATH:/opt/conda/lib/python3.7/site-packages:/opt/conda/lib/python3.7/site-packages/bin \
    CLASSPATH=$CLASSPATH:/opt/conda/lib/python3.7/site-packages/pyspark/jars/* \
    SPARK_CLASSPATH=$SPARK_CLASSPATH:/opt/conda/lib/python3.7/site-packages/pyspark/jars/*

COPY ./nyt2.json ./

RUN ln -s /opt/conda/lib/python3.7/site-packages/sparkmonitor/listener_2.12.jar /opt/spark/jars/listener_2.12.jar


