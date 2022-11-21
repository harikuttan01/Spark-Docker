FROM hareendranvr/driver-2

RUN mkdir ./Constants
COPY ./Constants ./Constants
COPY ./nyt2.json ./
COPY ./spark-session.py ./

CMD [ "python", "./spark-session.py" ]