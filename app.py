import os
from flask import Flask
from flask import jsonify
import time
import sys
from Neo4J import NeoDatabase
from Mongo import MongoDatabase
# import pymongo
from dotenv import dotenv_values
app = Flask(__name__)
app.config.from_object(__name__)

config = dotenv_values(".env")
# MONGO_URL = config.get("MONGO_URL")


@app.route("/heartbeat")
def home():
    return {"villeChoisie": "Montreal"}


@app.route('/extracted_data', methods=['GET'])
def extracted_data():

    dbNeo = NeoDatabase()
    Neodata = dbNeo.extracted_data_Neo()

    dbMongo = MongoDatabase()
    MongoData = dbMongo.extracted_data_Mongo()

    return {
        "nbRestaurants": MongoData,
        "nbSegments": Neodata
    }


@app.route("/transformed_data")
def transformed_data():

    dbNeo = NeoDatabase()
    Neodata = dbNeo.transformed_data_Neo()

    dbMongo = MongoDatabase()
    MongoData = dbMongo.transformed_data_Mongo()

    return {
        "restaurants": MongoData,
        "longueurCyclable": Neodata
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
