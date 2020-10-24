from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import logging

# Helper function to convert the table ticks to number
def convert_val(val):
    if val != "":
        return 1
    return 0

# Returns a dictionary with the languages (Interface, Audio and Subtitles) of the game
def get_languages(driver):
    try:
        # Some games (like NFL 21) don't support many languages, so this click is not necessary
        try:
            # Click to show all available languages first
            driver.find_element_by_css_selector(".all_languages").click()
        except NoSuchElementException:
            logging.debug("No show all languages button")

        # Get all languages
        categories = driver.find_elements_by_css_selector(".game_language_options tbody tr")
        index = []
        data = []
        columns = ['Interface', 'Full Audio', 'Subtitles']
        for i in range(1, len(categories)):
            index.append(categories[i].text.split(" ")[0])

        dict = {}
        rows = driver.find_elements_by_css_selector(".game_language_options tbody tr td")
        for i in range(0, len(rows)-3, 4):
            dict[rows[i].text] = [convert_val(rows[i+1].text), convert_val(rows[i+2].text), convert_val(rows[i+3].text)]
        
        data = dict.values()
        df = pd.DataFrame(data, index, columns)
        return df
    except NoSuchElementException:
	    logging.error("Cannot get languages table")
    return ""
    

# Get the release date from steam
def get_realease_date(driver):
    try:
        release_date = driver.find_element_by_css_selector(".user_reviews .release_date").text.split("\n")[1]
        return release_date
    except NoSuchElementException:
        logging.error("Cannot get release date")
    return ""
