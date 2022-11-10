FROM gcr.io/lti-coe/pyspark-base


WORKDIR /home
ARG shared_workspace=/opt/workspace
RUN pip install --upgrade pip
RUN pip install pyspark

COPY connect.py ./

ENV SHARED_WORKSPACE=${shared_workspace}

# -- Runtime

VOLUME ${shared_workspace}

CMD ["python", "./connect.py"]