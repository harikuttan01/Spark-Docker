FROM gcr.io/lti-coe/pyspark-base

WORKDIR /home

RUN pip install pyspark

COPY ./test.py ./
COPY ./nyt2.json ./

CMD ["python","./test.py"]