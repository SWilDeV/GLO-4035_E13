# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

COPY requirements.txt requirements.txt
COPY populate.py populate.py
COPY .env .env

RUN pip install -Ur requirements.txt

COPY . .

CMD [ "python", "app.py"]