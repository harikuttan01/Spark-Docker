
FROM itayb/spark:3.1.1-hadoop-3.2.0-aws

RUN mkdir -p /opt/conda/lib/python3.7/site-packages && \
    chmod 777 -R /opt/conda/lib/python3.7/site-packages && \
    ln -s python3.7 /usr/bin/python

RUN pip install \
    notebook==6.2.0 \
    ipynb==0.5.1 \
    sparkmonitor==1.1.1 \
    pyspark==3.1.1 --target=/opt/conda/lib/python3.7/site-packages

ENV PYTHONPATH=:/opt/conda/lib/python3.7/site-packages \
    PATH=$PATH:/opt/conda/lib/python3.7/site-packages:/opt/conda/lib/python3.7/site-packages/bin \
    CLASSPATH=$CLASSPATH:/opt/conda/lib/python3.7/site-packages/pyspark/jars/* \
    SPARK_CLASSPATH=$SPARK_CLASSPATH:/opt/conda/lib/python3.7/site-packages/pyspark/jars/*
# install extension to monitor spark
RUN jupyter nbextension install sparkmonitor --py --user --symlink && \
    jupyter nbextension enable  sparkmonitor --py && \
    jupyter serverextension enable --py --user --debug sparkmonitor && \
    ipython profile create && \
echo "c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')" >>  $(ipython profile locate default)/ipython_kernel_config.py

RUN ln -s /opt/conda/lib/python3.7/site-packages/sparkmonitor/listener_2.12.jar /opt/spark/jars/listener_2.12.jar

# Copying postgresql-42.5.0.jar
COPY postgresql-42.5.0.jar /opt/conda/lib/python3.7/site-packages/pyspark/jars
COPY postgresql-42.5.0.jar /opt/spark/jars/
RUN useradd -ms /bin/bash mosaic-ai -u 1001
USER mosaic-ai



