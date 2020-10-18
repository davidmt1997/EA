from selenium import webdriver
import pandas as pd

PATH = "/home/dmiranda/Development/python/ea/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

PES_STEAM_URL = "https://store.steampowered.com/app/996470/eFootball__PES_2020/"
FIFA_STEAM_URL = "https://store.steampowered.com/app/1313860/EA_SPORTS_FIFA_21/" #Fifa 21, can't find language for fifa 20

driver.get(FIFA_STEAM_URL)

# Click to show all available languages first
driver.find_element_by_css_selector(".all_languages").click()


# Get all languages
categories = driver.find_elements_by_css_selector(".game_language_options tbody tr")
index = []
data = []
columns = ['Interface', 'Full Audio', 'Subtitles']
for i in range(1, len(categories)):
    index.append(categories[i].text.split(" ")[0])

# TODO: find a way to get the languages
for i in categories:
    print(i.text)


release_date = driver.find_element_by_css_selector(".user_reviews .release_date").text
print(release_date)


driver.close()