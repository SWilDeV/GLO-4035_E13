# Monter les dockers

docker compose up

# Requêtes possibles :
## @GET /hearthbeat
### Exemple Requête:
/heartbeat <br />
### Result:
{<br />
  "villeChoisie": "Montreal"<br />
}

## @GET /extracted_data
### Exemple Requête:
/extracted_data <br />
### Result:
{<br />
  "nbRestaurants": 3857,<br />
  "nbSegments": 5470<br />
}

## @GET /transformed_data
### Exemple Requête:
/transformed_data <br />
### Result:
{<br />
  "longueurCyclable": "634258.0",<br />
  "restaurants": {<br />
    "Asiatique": 96,<br />
    "Bar laitier": 43,<br />
    "Bar salon, taverne": 291,<br />
[...]<br />
    "Restaurant service rapide": 103,<br />
    "Rotisserie": 73,<br />
    "Sushi": 179,<br />
    "Thai": 30,<br />
    "Tim Hortons": 46,<br />
    "Vietnamien": 51<br />
  }<br />
}<br />

## @GET /readme
### Exemple Requête:
/readme <br />
*Ouvre le document présent*

## @POST /starting_point
### Exemple Requête:
/starting_point <br />
### with payload: <br />
{<br />
    "length": 100,<br />
    "type": ["Italien", "Cafe"]<br />
}<br />
### Result:
{<br />
    "startingPoint": {<br />
        "coordinates": [<br />
            45.525085,<br />
            -73.555608<br />
        ],<br />
        "type": "Point"<br />
    }<br />
}<br />

# Web Server Dockerised (default): .env file:

NEO4J_CREDENTIALS=neo4j/secret_password_1234
NEO4J_URL=bolt://172.21.0.2:7687
MONGO_URL=mongodb://172.21.0.3:27017

# Local Web Server : .env file:

NEO4J_CREDENTIALS=neo4j/secret_password_1234
NEO4J_URL_LOCAL=bolt://localhost:7687
MONGO_URL_LOCAL=mongodb://localhost:27017

