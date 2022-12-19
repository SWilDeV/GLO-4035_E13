
from decouple import config
from py2neo import Graph


INTERNAL_URL = config("NEO4J_URL")
USERNAME, PASSWORD = config("NEO4J_CREDENTIALS").split("/")
graph = Graph(INTERNAL_URL, auth=(USERNAME, PASSWORD), secure=False)

# pour utiliser le graph dans gds
# cette commande on devrait la passer lors du populateNeo apres les insertions des points et relations.
graph.run('''
CALL gds.graph.project(
    'Graph',
    'PointCycle',
    'connecte',
    {
        relationshipProperties: 'longueur'
    }
)
''')

def parcours_point(graph, point_dep, distance, type, limite): 
    query = ('''
    MATCH (source:PointCycle)
    WHERE source.id_pointCycle = ''' +"'"+str(point_dep) +"'"+ '''
    CALL gds.allShortestPaths.dijkstra.stream('Graph', {
        sourceNode: source,
        relationshipWeightProperty: 'longueur',
        nodeLabels: ['PointCycle']
    })
    YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
    WHERE gds.util.asNode(targetNode).'''+type+''' > 1 AND totalCost > '''+str(distance*0.9)+''' AND totalCost < '''+str(distance*1.1)+''' AND gds.util.asNode(targetNode) <> gds.util.asNode(sourceNode)

    RETURN DISTINCT
        totalCost,
        gds.util.asNode(sourceNode).id_pointCycle AS sourceNodeId,
        gds.util.asNode(targetNode).id_pointCycle AS targetNodeId,
        [nodeId IN nodeIds | gds.util.asNode(nodeId).id_pointCycle] AS nodeNames
    ORDER BY 'totalCost'
    SKIP 1
    LIMIT '''+str(limite)+'''
    ''')
    return graph.begin().run(query).data()

def parcours_stops(graph, point_dep, arrets, distance, type, limite):
    liste_parcours=[]
    for element in parcours_point(graph, point_dep, distance/arrets, type, int(limite/arrets)):
        parcours = [element['totalCost'],element['targetNodeId'], element['nodeNames']]
        if arrets == 1: 
            liste_parcours.append(parcours)
            next
        else:
            for element_2 in parcours_point(graph, element['targetNodeId'], distance/arrets, type, int(limite/arrets)):
                parcours_2 = [parcours[0]+element_2['totalCost'], parcours[1],element_2['targetNodeId'],element['nodeNames']+element_2['nodeNames']]
                if arrets == 2: 
                    liste_parcours.append(parcours_2)
                    next
                else:
                    for element_3 in parcours_point(graph, element_2['targetNodeId'], distance/arrets, type, int(limite/arrets)):
                            parcours_3 = [parcours_2[0]+element_3['totalCost'], parcours[1], parcours_2[2],element_3['targetNodeId'],element['nodeNames']+element_2['nodeNames']+element_3['nodeNames']]
                            if arrets == 3:
                                liste_parcours.append(parcours_3)
    return liste_parcours
    


### parcours_stops(graph, point de depart, nombre_arrets, distance, type_resto, limite)
##  ATENTION avec limite!! pas trop grand, sinon ca va planter. Je le laisserai a 10

for element in parcours_stops(graph, 1207, 2, 2000, 'Pizzeria', 10):
    print (element)
