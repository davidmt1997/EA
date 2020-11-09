#from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import logging

# Returns the title of the game
def get_game_title(driver):
	try:
		title = driver.find_element_by_css_selector(".firstHeading")
		return title.text
	except NoSuchElementException:
		logging.error("Cannot get game title")
	return ""

# Returns the first paragraph of the page
# Currently not in use
def get_first_p(driver):
	try:
		words = driver.find_elements_by_css_selector(".mw-parser-output p")
		return words[1].text
	except NoSuchElementException:
		logging.error("Cannot get first paragraph")
	return ""

# Returns a dictionary with key pair values of the info table
def get_info_table(driver):
	ret = {}
	# Categories of the table we are interested in
	categories = ['Developer(s)', 'Publisher(s)', 'Series', 'Platform(s)', 'Mode(s)']
	try:
		rows = driver.find_elements_by_css_selector(".hproduct tbody tr")
		for i in range(2, len(rows)): # Skip the first two because its the title and an image
			# If the field found is not in the list, don't add it
			if rows[i].find_element_by_css_selector("th").text not in categories:
				continue
			ret[rows[i].find_element_by_css_selector("th").text] = preprocess(rows[i].find_element_by_css_selector("td").text)
	except NoSuchElementException:
		logging.error("Cannot get info table")

	return ret

# Returns a dictionary with key value pairs of the publications score table
def get_scores_table(driver):
	ret = {}
	try:
		scores = driver.find_elements_by_css_selector(".infobox.wikitable tbody tr td")
		for i in range(0, len(scores), 2): # Loop 2 by 2 to get the publication as key and the score as value
			# Skip empty scores
			if preprocess(scores[i+1].text)[0] != '':
				ret[scores[i].text] = preprocess(scores[i+1].text)
	except NoSuchElementException:
		logging.error("Cannot get scores table")
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
	


