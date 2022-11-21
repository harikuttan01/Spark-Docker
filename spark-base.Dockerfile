FROM python:3.7

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    curl \
    git

RUN apt-get update && apt-get install -y \
    software-properties-common

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN apt update -y && \
    apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' && apt update -y && \
    apt-get install -y openjdk-8-jdk-headless --fix-missing && \
    export JAVA_HOME && \
    apt-get clean


ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# COPY ./requ.txt ./requ.txt
# RUN pip install -r requ.txt
RUN pip install --no-cache-dir pyspark==3.1.1 ipynb==0.5.1 kubernetes==9.0.0 wget

COPY ./jars/ /usr/local/lib/python3.7/site-packages/pyspark/jars/

ENV SPARK_LOCAL_IP localhost
RUN export SPARK_LOCAL_IP

RUN unset SPARK_HOME

ENV PYTHONPATH=/usr/local/lib/python3.7/site-packages/pyspark/python:/usr/local/lib/python3.7/site-packages/pyspark/python/lib/py4j-0.10.9-src.zip:${PYTHONPATH}
RUN export PYTHONPATH

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools