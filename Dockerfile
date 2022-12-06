# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster
RUN pip install --upgrade pip

WORKDIR /app


COPY populate_neo4j.py populate_neo4j.py
COPY populate_mongo.py populate_mongo.py
COPY data_full.csv data_full.csv
COPY data_short.csv data_short.csv
COPY dataV3_short.csv dataV3_short.csv
COPY data_dev.csv data_dev.csv
COPY intersection_extremites_short.csv intersection_extremites_short.csv
COPY multinodes_extremites_short.csv multinodes_extremites_short.csv
COPY basicRelations_short.csv basicRelations_short.csv
COPY intersection_short.csv intersection_short.csv
COPY intersection.csv intersection.csv
COPY businesses.geojson businesses.geojson
COPY app.py app.py
COPY Mongo.py Mongo.py
COPY Neo4J.py Neo4J.py
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip install -Ur requirements.txt
