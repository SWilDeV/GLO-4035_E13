# Database
from dotenv import dotenv_values
from py2neo import Graph

config = dotenv_values(".env")
INTERNAL_URL = config.get("NEO4J_URL")
USERNAME, PASSWORD = config.get("NEO4J_CREDENTIALS").split("/")


class NeoDatabase:

    def extracted_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep = int(
                (f'{(TRANSACTION.run("MATCH p=()-[r:connecte]->() RETURN count(p) as total").data()[0]["total"])}'))


        except:
            print("prb Neo extracted data")
            return "prb Neo extracted data"

        else:
            return rep

    def transformed_data_Neo(self):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            rep = (f'{(TRANSACTION.run("MATCH (:PointCycle)-[r:connecte]->(:PointCycle) return  sum(r.longueur) as total").data()[0]["total"])}')


        except:
            print("prb Neo transformed data")
            return "prb Neo transformed data"

        else:
            return rep

    def adjacent(self, id):
        listAdj = []
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            request = 'MATCH (a:PointCycle {id_pointCycle:"' + id + '"})-[connecte]->(b:PointCycle) RETURN b.id_pointCycle'
            rep = ((TRANSACTION.run(request).data()))
        except:
            print("failed request path from node")
            return "failed request path from node : " + request
        else:
            for x in rep:
                listAdj.append(x["b.id_pointCycle"])
            return listAdj

    def paths(self, id, nNodes):
        listPaths = [[id]]
        i = nNodes
        while i > 1:
            newListPath = []
            for path in listPaths:
                currentNode = path[len(path) - 1]
                adjNodes = self.adjacent(currentNode)
                for newNode in adjNodes:
                    newListPath = newListPath + [path + [newNode]]
            i = i - 1
            listPaths = newListPath
        return listPaths
