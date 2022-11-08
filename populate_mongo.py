import pymongo
from dotenv import dotenv_values
import geojson
config = dotenv_values(".env")
MONGO_URL = config.get("MONGO_URL")

client = pymongo.MongoClient(MONGO_URL)
db = client["travaille_longitudinal"]
file_resto = open("businesses.geojson", encoding="utf8")
datadb = geojson.load(file_resto)
col = db["travaille_longitudinal_data"]
col.insert_many(data for data in datadb["features"])
file_resto.close()