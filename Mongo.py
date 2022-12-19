# Database
import pymongo
import sys
import random
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

    def queryMongoDBForNeoData(self, data, type):
        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client["t_long"]
            col = db["t_long_col"]
            finalArray = []

            # All the Neo4J Points in the path are in data
            for element in data:
                NodeCoordinates = []
                NodeCoordinates.append(element[1])
                NodeCoordinates.append(element[2])

                pipeline = [
                    {
                        "$match": {
                            "geometry": {"$geoWithin": {
                                "$centerSphere": [[element[1], element[2]], 0.5 / 6378]}},

                            "properties.type": type

                        },

                    }
                ]
                # All restaurants per Neo4J Point are in results
                restos = list(col.aggregate(pipeline))
                randomNum = random.randint(0, len((restos))-1)
                # print(randomNum)
                nomResto = restos[randomNum]["properties"]["name"]
                restoCoord = restos[randomNum]["geometry"]["coordinates"]
                restoArray = []
                isPresent = False
                for row in finalArray:
                    if (row[3] == restoCoord):
                        isPresent = True
                if isPresent == False:
                    restoArray.append(element[0])
                    restoArray.append(NodeCoordinates)
                    restoArray.append(nomResto)
                    restoArray.append(restoCoord)
                    finalArray.append(restoArray)

            return finalArray
        except:
            print("Oops!", sys.exc_info()[1], "occurred.")

    def extracted_type_Mongo(self):

        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client["t_long"]
            col = db["t_long_col"]

        except:
            print("Oops!", sys.exc_info()[1], "occurred.")
            print("error with Mongo Connexion in extracted_data")
            return "error with Mongo Connexion in extracted_data"

        else:
            return col.distinct("properties.type")
