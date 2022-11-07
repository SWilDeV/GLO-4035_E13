# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster

WORKDIR /app


COPY populate_etape2.py populate_etape2.py
COPY app.py app.py
COPY Neo4J.py Neo4J.py
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip install -Ur requirements.txt

CMD ["python3","app.py"]