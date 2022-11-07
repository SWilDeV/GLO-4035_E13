

//docker run -it --name resto mongo:5.0
//docker exec -it resto mongo

//pour exporter la base de données j'ai utilisé cette comamnde
//docker exec resto mongoexport --collection=resto --db=resto --out resto.json   


//commande utilisé pour insérer les documents à la base de données
db.resto.insert(
{ "type": "Feature", "properties": { "business_id": 127, "name": "LES ENTREPRISES ALJO", "address": "12515   Boulevard Rodolphe-Forget ", 
"city": "Montréal", "state": "Québec, Canada", "type": "Distributrice automatique", "statut": "Ouvert", "date_statut": "20031123", 
"latitude": "45.650661", "longitude": "-73.580264", "x": 298544.13, "y": 5056754.99 }, 
"geometry": { "type": "Point", "coordinates": [ -73.580263608359701, 45.650660588882545 ] } }
)


db.resto.remove( {"properties.statut": { $not: {$regex: "Ouvert"}}})
db.resto.distinct("properties.type" )
type_a_garder = 
[
        "Bar laitier",
        "Bar laitier saisonnier",
        "Bar salon, taverne",
        "Boulangerie",
        "Brasserie",
        "Café, thé, infusion, tisane",
        "Cafétéria",
        "Casse-croûte",
        "Distributrice automatique",
        "Pâtisserie",
        "Restaurant",
        "Restaurant mets pour emporter",
        "Restaurant service rapide",
        "Épicerie avec préparation"
]

db.resto.find().pretty()
db.resto.remove( {"properties.type": { $nin: type_a_garder}}) 
WriteResult({ "nRemoved" : 7237 })
db.resto.count()
// croissement des rues Berri et maisonneuve est  45.515297, -73561084
depart_parcours = {"coordinates": [-73.561084, 45.515297]}

db.resto.count()

db.resto.createIndex({"geometry" : "2dsphere"})
db.resto.getIndexes()

db.resto.count({ "geometry":{"$near": { "$geometry": {  "type": "Point", "coordinates": [-73.561084, 45.515297]} , "$maxDistance": 1000}}})
db.resto.find({"geometry" : { "$nearSphere" : {"$geometry": {  "type": "Point", "coordinates" : depart_parcours.coordinates } ,  "$maxDistance": 1000}}}).pretty()



