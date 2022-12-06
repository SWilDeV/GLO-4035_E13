# Database
import pymongo
from dotenv import dotenv_values

config = dotenv_values(".env")
MONGO_URL = config.get("MONGO_URL")


class MongoDatabase:

    def extracted_data_Mongo(self):

        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client["t_long"]
            col = db["t_long_col"]

        except:
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("error with Mongo Connexion in extracted_data")
            return "error with Mongo Connexion in extracted_data"

        else:
            return col.count_documents({})

    def transformed_data_Mongo(self):
        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client["t_long"]
            col = db["t_long_col"]

        except:
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("error with Mongo Connexion in transformed_data")
            return "error with Mongo Connexion in transformed_data"

        else:
            result = {}
            restos = col.distinct("properties.type")
            for resto in restos:
                count = col.count_documents({"properties.type": resto})
                result[resto] = count

            return result
