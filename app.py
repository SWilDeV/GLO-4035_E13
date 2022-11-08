import os
from flask import Flask
from flask import jsonify
import time
import sys
from Neo4J import Database
import pymongo
from dotenv import dotenv_values
app = Flask(__name__)
app.config.from_object(__name__)

config = dotenv_values(".env")
MONGO_URL = config.get("MONGO_URL")


@app.route("/heartbeat")
def home():
    return {"Montreal":"str"}


@app.route('/extracted_data', methods=['GET'])
def extracted_data():
    try:
        db=Database()
        data = db.extracted_data_Neo()

        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client["t_long"]
            col = db["t_long_col"]
        
        except:
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("error with Mongo Connexion in extracted_data")
            return "error with Mongo Connexion in extracted_data"
        
        
    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print("error with extracted_data")
        return "error with extracted_data "
    else:
        return {
        "nbRestaurants":"int",
         "nbRestaurants":col.count_documents({}),
        "nbSegments":data
        }


@app.route("/transformed_data")
def transformed_data():
    try:
        db=Database()
        data = db.transformed_data_Neo()

        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client["t_long"]
            col = db["t_long_col"]
        
        except:
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("error with Mongo Connexion in transformed_data")
            return "error with Mongo Connexion in transformed_data"

    except:
        print("Oops!", sys.exc_info()[1], "occurred.")
        print("error with transformed_data")
        return "error with transformed_data"
    else:
        result = []
        restos = col.distinct("properties.type")
        for resto in restos:
            count = col.count_documents({"properties.type":resto})
            result.append({resto:count})
  
        return {
            "restaurants":result,
            "longueurCyclable":data
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)