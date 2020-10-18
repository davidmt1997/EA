from py2neo import Graph, Node, Relationship
from scrapper import *
graph = Graph("bolt://neo4j:gland-inception-surveyor@52.86.147.25:33217")

FIFA_WIKI_URL = "https://en.wikipedia.org/wiki/FIFA_20"
PES_WIKI_URL = "https://en.wikipedia.org/wiki/EFootball_PES_2020"

PATH = "/home/dmiranda/Development/python/ea/chromedriver_linux64/chromedriver"
driver1 = webdriver.Chrome(PATH)
driver2 = webdriver.Chrome(PATH)


# Modify the url to switch the games page
driver1.get(PES_WIKI_URL)

# TODO: maybe do this in a loop?
game1 = get_game_title(driver1)
info1 = get_info_table(driver1)
driver1.close()

driver2.get(FIFA_WIKI_URL)
game2 = get_game_title(driver2)
info2 = get_info_table(driver2)
driver2.close()


# TODO: change relationships to make better visualizations
tx = graph.begin()
a = Node("Game", name=game1)
for x, y in info1.items():
	r1 = Relationship(a, x, y)
	tx.create(r1)

tx.create(a)
b = Node("Game", name=game2)
for x, y in info2.items():
	r2 = Relationship(b, x, y)
	tx.create(r2)

tx.commit()

print("Done")
