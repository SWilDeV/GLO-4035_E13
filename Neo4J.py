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


    # la fonction peut etre bonifie
    # elle return toutes les plus courts chemins vers les autres Nodes
    # en format list, cela nous permet de parcourir toutes les sorties

    def Dijkstra(self, id):
        GRAPH = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD))
        TRANSACTION = GRAPH.begin()
        try:
            request = ('''
                        MATCH (source:PointCycle)
                        WHERE source.id_pointCycle = ''' +"'"+str(id) +"'"+ '''
                        CALL gds.allShortestPaths.dijkstra.stream('Graph', {
                            sourceNode: source,
                            relationshipWeightProperty: 'longueur',
                            nodeLabels: ['PointCycle']
                        })
                        YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
                        RETURN
                            index,
                            gds.util.asNode(sourceNode).id_pointCycle AS sourceNodeId,
                            gds.util.asNode(targetNode).id_pointCycle AS targetNodeId,
                            gds.util.asNode(targetNode).arrond AS arrondNodeId,
                            totalCost,
                            [nodeId IN nodeIds | gds.util.asNode(nodeId).id_pointCycle] AS nodeNames,
                            costs,
                            nodes(path) as path
                        ORDER BY totalCost
                        ''')
            rep = ((TRANSACTION.run(request).data()))


        except:
            print("failed request Dijkstra from node")
            return "failed request Dijkstra from node : " + id

        else:
            return rep


