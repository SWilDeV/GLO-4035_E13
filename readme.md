# Monter les dockers

docker compose up

# .env file:

NEO4J_CREDENTIALS=neo4j/secret_password_1234
NEO4J_URL=bolt://172.21.0.2:7687
MONGO_URL=mongodb://172.21.0.3:27017

# Utilisation en local avec le docker ouvert
NEO4J_CREDENTIALS=neo4j/secret_password_1234
NEO4J_URL_LOCAL=bolt://localhost:7687
MONGO_URL_LOCAL=mongodb://localhost:27017

# attente ~15 min
