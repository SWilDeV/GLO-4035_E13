import pymongo
import time
from dotenv import dotenv_values
import geojson



config = dotenv_values(".env")
MONGO_URL = config.get("MONGO_URL")


print('Waiting for servers connections')


# We wait for services Mongo to start
def validate_mongo_connection(url):
    try:
        print('Trying connection to Mongo')
        client = pymongo.MongoClient(MONGO_URL)
        db = client["test_Connexion"]

        print('mongo connection works')
    except:
        print('Connection to mongo failed, will retry in 5 sec')
        time.sleep(5)
        validate_mongo_connection(url=url)


validate_mongo_connection(url=MONGO_URL)


client = pymongo.MongoClient(MONGO_URL)
db = client["t_long"]
file_resto = open("businesses.geojson", encoding="utf8")
datadb = geojson.load(file_resto)

col = db["t_long_col"]
col.insert_many(data for data in datadb["features"])

file_resto.close()