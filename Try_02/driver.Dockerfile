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

RUN pip install --no-cache-dir pyspark==3.1.1 ipynb==0.5.1 kubernetes==9.0.0 wget

RUN mkdir ./Constants
COPY ./Constants ./Constants
COPY ./spark-session.py ./

CMD [ "python", "./spark-session.py" ]