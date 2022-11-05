import time
import csv

from decouple import config
from py2neo import Graph, Node, Relationship


INTERNAL_URL = config("NEO4J_INTERNAL_URL")

# We use split to split the NEO4J_AUTH formatted as "user/password"
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")

print('Waiting for servers connections')


# We wait for services Neo4J to start
def validate_neo_connection(url, username, password):
    try:
        print('Trying connection to neo')
        Graph(
            url,
            auth=(username, password),
            secure=False
        )
        print('neo connection works')
    except:
        print('Connection to neo failed, will retry in 10 sec')
        time.sleep(10)
        validate_neo_connection(url=url, username=username, password=password)


validate_neo_connection(url=INTERNAL_URL, username=USERNAME, password=PASSWORD)

graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)
transaction = graph.begin()
#WGS84Point = _point_subclass("WGS84Point", ["longitude", "latitude", "height"], {2: 4326, 3: 4979})


filename = 'data2.csv'

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    counter = 1;
    for row in datareader:
        # row[0]= Node("Point", IDPiste=row[1], Quartier=row[2], longitude=row[3], latitude=row[4], IdPoint=row[0])
        graph.run(f"CREATE (p:PointCycle) SET p.location = Point({{latitude: {row[4]}, longitude: {row[3]}}}),  p.Quartier = '{row[2]}',  p.IDPiste = '{row[1]}',  p.IdPoint = '{row[0]}'")
        counter +=1
        #transaction.create(row[0])
    
    #quebec = Node("Ville", fondation=1608, population=550294, altitude=98, langues="français", nom="Québec")
    #transaction.create(quebec)
    print(counter)


#graph.delete_all()
#graph.commit(transaction)
