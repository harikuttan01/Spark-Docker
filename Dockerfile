FROM gcr.io/lti-coe/pyspark-base

WORKDIR /home

RUN pip install pyspark

COPY ./test.py ./

CMD ["python","./test.py"]