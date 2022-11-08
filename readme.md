# Monter les dockers

docker compose up

# Web Server Dockerised (default): .env file:

NEO4J_CREDENTIALS=neo4j/secret_password_1234
NEO4J_URL=bolt://172.21.0.2:7687
MONGO_URL=mongodb://172.21.0.3:27017

# Local Web Server : .env file:

NEO4J_CREDENTIALS=neo4j/secret_password_1234
NEO4J_URL_LOCAL=bolt://localhost:7687
MONGO_URL_LOCAL=mongodb://localhost:27017

# Potentielle attente ~15 min
Si utilisation des donnees de pistes cyclable complete. Sinon utiliser la version data_short (defaut) qui est un extrait des donnees completes.
Le choix se fait a la ligne 21 du fichier populate_neo4J.py, en remplacant "data_short.csv" par "data_full.csv" 
