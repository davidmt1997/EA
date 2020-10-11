from py2neo import Graph, Node, Relationship
graph = Graph("bolt://neo4j:gland-inception-surveyor@52.86.147.25:33217")

tx = graph.begin()
a = Node("Person", name="Alice")
tx.create(a)
b = Node("Person", name="Bob")

ab = Relationship(a, "KNOWS", b)
tx.create(ab)

tx.commit()

print(graph.exists(ab))