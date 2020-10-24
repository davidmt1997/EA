from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import logging
import pandas as pd

# Returns a dataframe with the commentary table from the es pages
def get_commentaries(driver):
    tables = driver.find_elements_by_css_selector(".wikitable")
    data = {'Region': [],
            'Idioma': [],
            'Comentarista': []}
    df = pd.DataFrame(data)

    # Check if we find a table that contains a header
    try:
        for table in tables:
            header = table.find_element_by_css_selector("thead tr").text
            if header == "Región Idioma Comentaristas":
                rows = table.find_elements_by_css_selector("tbody tr")
                for row in rows:
                    tdata = row.find_elements_by_css_selector("td")
                    new_row = {'Region': tdata[0].text, 'Idioma': tdata[1].text, 'Comentarista': preprocess(tdata[2].text)}
                    df = df.append(new_row, ignore_index=True)
                break
    except NoSuchElementException:
        logging.error("Cannot find header in table")

    # Check if we find a table that the first row is the info we want
    try:
        for table in tables:
            header = table.find_elements_by_css_selector("tbody tr")
            if header[0].text == "Idioma Región Comentarista(s) Notas":
                for i in range(1, len(header)):
                    tdata = header[i].find_elements_by_css_selector("td")
                    if len(tdata) == 2:
                        x = header[i-1].find_elements_by_css_selector("td")[0].text
                        tdata.insert(0, x)
                        new_row = {'Region': tdata[1].text, 'Idioma': tdata[0], 'Comentarista': preprocess(tdata[2].text)}
                    else:
                        new_row = {'Region': tdata[1].text, 'Idioma': tdata[0].text, 'Comentarista': preprocess(tdata[2].text)}
                    df = df.append(new_row, ignore_index=True)
                break
    except NoSuchElementException:
        logging.error("Cannot find table")
    
    return df

def preprocess(word):
    return word.replace("\n", ",")

