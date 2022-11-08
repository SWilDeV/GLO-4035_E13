import pymongo
import time
from dotenv import dotenv_values
import geojson

config = dotenv_values(".env")
MONGO_URL = config.get("MONGO_URL")


print('Waiting for servers connections')


# We wait for services Mongo to start
def populate_mongo(url):
    try:
        print('Trying connection to Mongo')
        client = pymongo.MongoClient(MONGO_URL)
        db = client["t_long"]

        file_resto = open("businesses.geojson", encoding="utf8")
        datadb = geojson.load(file_resto)

        col = db["t_long_col"]
        col.insert_many(data for data in datadb["features"])

        file_resto.close()

        print('Mongo Data inserted !')
    except:
        print('Connection to mongo failed, will retry in 5 sec')
        time.sleep(5)
        populate_mongo(url=url)


populate_mongo(url=MONGO_URL)


