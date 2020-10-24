from py2neo import Graph, Node, Relationship
from wiki_scrapper import get_game_title, get_info_table, get_scores_table
from steam_scrapper import get_languages, get_realease_date
from wiki_es_scrapper import get_commentaries
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import logging
from selenium_driver import Selenium_driver

#graph = Graph("bolt://neo4j:gland-inception-surveyor@52.86.147.25:33217")

FIFA_WIKI_URL = "https://en.wikipedia.org/wiki/FIFA_20"
PES_WIKI_URL = "https://en.wikipedia.org/wiki/EFootball_PES_2020"
FIFA_WIKI_ES_URL = "https://es.wikipedia.org/wiki/FIFA_20"
PES_WIKI_ES_URL = "https://es.wikipedia.org/wiki/EFootball_Pro_Evolution_Soccer_2020"
PES_STEAM_URL = "https://store.steampowered.com/app/996470/eFootball__PES_2020/"
FIFA_STEAM_URL = "https://store.steampowered.com/app/1313860/EA_SPORTS_FIFA_21/" #Fifa 21, can't find language for fifa 20
NHL_WIKI_URL = "https://en.wikipedia.org/wiki/NHL_21"
NFL_WIKI_URL = "https://en.wikipedia.org/wiki/Madden_NFL_21"
NFL_STEAM_URL = "https://store.steampowered.com/app/1239520/Madden_NFL_21/"

'''
for url in [FIFA_WIKI_URL, PES_WIKI_URL, NHL_WIKI_URL, NFL_WIKI_URL]:
	my_driver = Selenium_driver(url)
	driver = my_driver.connect_driver()
	logging.info("Getting game title")
	game = get_game_title(driver)
	print(game)
	logging.info("Getting basic info table")
	info = get_info_table(driver)
	print(info)
	logging.info("Getting scores table")
	scores = get_scores_table(driver)
	print(scores)
	my_driver.diconnect_driver()


for url in [FIFA_WIKI_URL, PES_WIKI_URL, NHL_WIKI_URL, NFL_WIKI_URL]:
	my_driver = Selenium_driver(url)
	driver = my_driver.connect_driver()
	logging.info("Getting game title")
	game = get_game_title(driver)
	print(game)
	logging.info("Getting basic info table")
	info = get_info_table(driver)
	print(info)
	logging.info("Getting scores table")
	scores = get_scores_table(driver)
	print(scores)
	my_driver.diconnect_driver()

for url in [FIFA_WIKI_ES_URL, PES_WIKI_ES_URL, NFL_WIKI_URL]:
	my_driver = Selenium_driver(url)
	driver = my_driver.connect_driver()
	logging.info("Getting commentaries table")
	print(get_commentaries(driver))
	my_driver.diconnect_driver()
	

for url in [FIFA_STEAM_URL, PES_STEAM_URL, NFL_STEAM_URL]:
	my_driver = Selenium_driver(url)
	driver = my_driver.connect_driver()
	logging.info("Getting languages table")
	languages = get_languages(driver)
	print(languages)
	logging.info("Getting release date")
	release_date = get_realease_date(driver)
	print(release_date)
	my_driver.diconnect_driver()'''



# TODO: get social media scores and trending comparisons

'''
driver1 = webdriver.Chrome(PATH)
driver2 = webdriver.Chrome(PATH)


# Modify the url to switch the games page
driver1.get(PES_WIKI_URL)

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
'''
print("Done")
