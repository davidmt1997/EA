from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

FIFA_WIKI_URL = "https://en.wikipedia.org/wiki/FIFA_20"
PES_WIKI_URL = "https://en.wikipedia.org/wiki/EFootball_PES_2020"

# Returns the title of the game
def get_game_title(driver):
	title = driver.find_element_by_css_selector(".firstHeading i")
	return title.text

# Returns the first paragraph of the page
def get_first_p(driver):
	words = driver.find_elements_by_css_selector(".mw-parser-output p")
	return words[1].text

# Returns a dictionary with key pair values of the info table
def get_info_table(driver):
	ret = {}
	rows = driver.find_elements_by_css_selector(".hproduct tbody tr")
	for i in range(2, len(rows)): # Skip the first two because its the title and an image
		ret[rows[i].find_element_by_css_selector("th").text] = preprocess(rows[i].find_element_by_css_selector("td").text)

	return ret

# Returns a dictionary with key value pairs of the publications score table
def get_scores_table(driver):
	ret = {}
	scores = driver.find_elements_by_css_selector(".infobox.wikitable tbody tr td")
	for i in range(0, len(scores), 2): # Loop 2 by 2 to get the publication as key and the score as value
		ret[scores[i].text] = preprocess(scores[i+1].text)
	
	return ret

# Preprocessing helper function to split the scraped info from tables and remove the '[number]' clause 
def preprocess(words):
	words = words.split('\n')
	ret = []
	for word in words:
		if word.find('[') != -1:
			start = word.find('[')
			end = word.find(']')
			word = word[:start] + word[end+1:]
		ret.append(word)
	return ret
	

PATH = "/home/dmiranda/Development/python/ea/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

# Modify the url to switch the games page
driver.get(PES_WIKI_URL)

#print("Game title: ", get_game_title(driver))

#print("First paragraph: ", get_first_p(driver))

ret = get_info_table(driver)
for x, y in ret.items():
	print(x, y) 


ret = get_scores_table(driver)
for x, y in ret.items():
	print(x, y) 

driver.close()

