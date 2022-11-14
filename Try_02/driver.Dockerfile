FROM itayb/jupyter-notebook:6.2.0-spark-3.1.1-java-11-hadoop-3.2.0


# installing java
RUN apt-get update && \
    apt-get install -y ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

RUN pip config  unset global.target && \
    pip install --no-cache-dir pyspark==3.1.1 ipynb==0.5.1 kubernetes==9.0.0 && \
    pip config  set global.target /tmp/pip_packages     # pip package installation path [read only root file system]

# MOSAIC NB Custom Extensions
# RUN git clone https://deploy:_-NMgQspSvwJZGsK7LSj@git.lti-aiq.in/mosaic-ai-logistics/mosaic_nb_extension.git && \
#     jupyter nbextension install mosaic_nb_extension/spark_distributed_session/ && \
#     jupyter nbextension enable spark_distributed_session/main

# # Copying postgresql-42.5.0.jar
# COPY postgresql-42.5.0.jar /opt/conda/lib/python3.7/site-packages/pyspark/jars/
USER mosaic-ai
COPY spark-session.py ./

CMD ["python", "./spark-session.py"]
# ENTRYPOINT ["bash", "/entrypoint.sh"]