FROM gcr.io/lti-coe/pyspark-base
USER root
WORKDIR /home

RUN mkdir ./Constants
COPY ./Constants ./Constants


ARG shared_workspace=/opt/workspace
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install pyspark

COPY spark-session.py ./
COPY connect.py ./
USER mosaic-ai

ENTRYPOINT ["bash", "/entrypoint.sh"]
CMD ["python", "./spark-session.py"]
