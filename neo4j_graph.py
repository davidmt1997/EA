from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher


# Custom class to manage call to Neo4j 
class Neo_Graph:

    '''
    Constructor to create the graph, authentication passed
    '''
    def __init__(self):
        self.graph = Graph(password="")
        self.tx = None

    '''
    Function to begin the transactions with the graph
    '''
    def begin_transaction(self):
        self.tx = self.graph.begin()

    '''
    Custom node creator
    Arguments:
        type: Node type (type string)
        name: name of the node (type string)
    '''
    def create_node(self, node_type, name):
        n = Node(node_type, name=name)
        return n
        
    
    '''
    Custom Relationship creator
    Arguments:
        node1: Origin node (type Node)
        type: type of relationship (type string)
        node2: Destination node (type Node)
    '''
    def create_relationship(self, node1, rel_type, node2):
        r = Relationship(node1, rel_type, node2)
        self.tx.create(r)
        

    '''
    Custom commit call to commit the relationships created
    '''
    def commit(self):
        self.tx.commit()
