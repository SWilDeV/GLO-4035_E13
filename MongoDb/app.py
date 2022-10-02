import os
from flask import Flask
from flask_pymongo import PyMongo
from neo4j import GraphDatabase


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
print("Connected to mongo !")
db = mongo.db

driver = GraphDatabase.driver("bolt://52.72.13.205:47929", auth=basic_auth("neo4j", "knock-cape-reserve"))


@app.route("/heartbeat")
def home():
    return {"Montreal":"str"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)