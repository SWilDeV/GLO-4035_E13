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
        col.delete_many({})
        col.insert_many(data for data in datadb["features"])

        query_open = {"properties.statut": {"$not": {"$regex": "Ouvert"}} }
        col.delete_many(query_open)

        types_a_effacer = ["Aliments naturels","Atelier de conditionnement de produits de la pêche","Autres","Boucherie","Boucherie-épicerie","Cabane à sucre","Cafétéria institution d'enseignement","Camion de distribution de produits carnés","Camion de distribution de produits de la pêche","Camion de distribution de produits laitiers","Camion-cuisine","Camp de vacances","Cantine mobile","Casse-croûte","Centre d'accueil","Charcuterie","Charcuterie/fromage","Confiserie/chocolaterie","Cuisine domestique","Distributeur en gros d'eau","Distributeur en gros de fruits et légumes frais","Distributeur en gros de produits carnés","Distributeur en gros de produits de la pêche","Distributeur en gros de produits laitiers","Distributeur en gros de produits mixtes","Distributeur en gros de succédanés de produits laitiers","Entrepôt","Entrepôt d'eau","Entrepôt de produits laitiers","Entrepôt de produits mixtes","Entrepôt de produits végétaux","Fabrique de boissons gazeuses","Fruits et légumes prêts à l'emploi","Garderie","Hôpital","Kiosque","Local de préparation","Magasin à rayons","Marché public","Noix et arachides","Organisme d'aide alimentaire","Poissonnerie","Produits à base de protéines végétales","Pâtes alimentaires","Pâtisserie","Pâtisserie-dépôt","Résidence de personnes âgées","Site d'eau vendue au volume","Supermarché","Traiteur","Usine d'embouteillage d'eau","Usine de produits laitiers","Usine de produits marins","Usine produit autre","Vendeur itinérant","Véhicule livraison","École/mesures alimentaires","Épicerie","Événements spéciaux"]
        for element in types_a_effacer:
            col.delete_many({"properties.type": { "$regex": element}})

        file_resto.close()

        print('Mongo Data inserted !')
    except:
        print('Connection to mongo failed, will retry in 5 sec')
        time.sleep(5)
        populate_mongo(url=url)


populate_mongo(url=MONGO_URL)


