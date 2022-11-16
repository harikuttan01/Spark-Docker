FROM gcr.io/lti-coe/pyspark-base
USER root
WORKDIR /home

RUN mkdir ./Constants
COPY ./Constants ./Constants


ARG shared_workspace=/opt/workspace
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install pyspark
COPY sm.py ./
COPY connect.py ./

CMD ["python", "./sm.py"]
