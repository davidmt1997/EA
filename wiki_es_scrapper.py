from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import logging
import pandas as pd
import spacy

nlp = spacy.load('es_core_news_lg')


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
            #if header == "Región Idioma Comentaristas":
            if "Comentaristas" in header:
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

# Returns a X with the different licenses of the team
def get_fifa_licenses_table(driver):
    # Find all the tables
    tables = driver.find_elements_by_css_selector(".wikitable")
    count = 0
    found = 0
    data = {'Competicion': [],
            'Pais': [],
            'Club': [],
            'Licencia': []}
    df = pd.DataFrame(data)
    data2 = {'Pais': [],
            'Licencia': [],
            'Jugadores reales': []}
    data3 = {'Pais': [],
            'Jugadoras reales': []}
    selec_masc = pd.DataFrame(data2)
    selec_fem = pd.DataFrame(data3)
    try:
        for table in tables:
            header = table.find_element_by_css_selector("tbody tr").text
            # count the number of tables that contain these keywords
            if "reales" in header or "Licencia" in header:
                count += 1

        for table in tables:
            header = table.find_element_by_css_selector("tbody tr").text
            # Find the tables with the keywords
            if "reales" in header or "Licencia" in header:
                found += 1
                rows = table.find_elements_by_css_selector("tbody tr")
                country = ""
                for row in rows:
                    tdata = row.find_elements_by_css_selector("td")
                    # Skip the first row
                    if len(tdata) == 0:
                        continue
                    # If first table found
                    if found == 1:
                        if len(tdata) == 5:
                            country = tdata[2].text
                            new_row = {'Competicion':'Conmebol Libertadores', 'Pais': country, 'Club': tdata[3].text, 'Licencia': preprocess(tdata[4].text)}
                        if len(tdata) == 3:
                            country = tdata[0].text
                            new_row = {'Competicion':'Conmebol Libertadores', 'Pais': country, 'Club': tdata[1].text, 'Licencia': preprocess(tdata[2].text)}
                        if len(tdata) == 2:
                            new_row = {'Competicion':'Conmebol Libertadores', 'Pais': country, 'Club': tdata[0].text, 'Licencia': preprocess(tdata[1].text)}
                        df = df.append(new_row, ignore_index=True)
                    # If second table found
                    if found==2:
                        if len(tdata) == 5:
                            country = tdata[2].text
                            new_row = {'Competicion':'Conmebol Sudamericana', 'Pais': country, 'Club': tdata[3].text, 'Licencia': preprocess(tdata[4].text)}
                        if len(tdata) == 3:
                            country = tdata[0].text
                            new_row = {'Competicion':'Conmebol Sudamericana', 'Pais': country, 'Club': tdata[1].text, 'Licencia': preprocess(tdata[2].text)}
                        if len(tdata) == 2:
                            new_row = {'Competicion':'Conmebol Sudamericana', 'Pais': country, 'Club': tdata[0].text, 'Licencia': preprocess(tdata[1].text)}
                        df = df.append(new_row, ignore_index=True)
                    # If third table found
                    if found == 3:
                        if len(tdata) == 4:
                            new_row = {'Pais': tdata[1].text, 'Licencia': tdata[2].text, 'Jugadores reales': preprocess(tdata[3].text)}
                        if len(tdata) == 3:
                            new_row = {'Pais': tdata[0].text, 'Licencia': tdata[1].text, 'Jugadores reales': preprocess(tdata[2].text)}
                        selec_masc = selec_masc.append(new_row, ignore_index=True)
                    
                    # If fourth table found
                    if found == 4:
                        if len(tdata) == 3:
                            new_row = {'Pais': tdata[1].text, 'Jugadoras reales': preprocess(tdata[2].text)}
                        if len(tdata) == 2:
                            new_row = {'Pais': tdata[0].text, 'Jugadoras reales': preprocess(tdata[1].text)}
                        selec_fem = selec_fem.append(new_row, ignore_index=True)
                # Stop writting when the number of found tables is the same as the count           
            if found == count:
                break

        print(df)
        print(selec_masc)
        print(selec_fem)
    except NoSuchElementException:
        print("Cannot find table") 

def get_pes_licenses_table(driver):
    data1 = {'Region': [],
            'Competicion': [],
            'Licencia': []}
    data2 = {'Region': [],
            'Seleccion': [],
            'Licencia': []}
    competiciones = pd.DataFrame(data1)
    selecciones = pd.DataFrame(data2)
    count = 0
    found = 0
    # Find all the tables
    tables = driver.find_elements_by_css_selector(".wikitable")
    try:
        for table in tables:
            header = table.find_elements_by_css_selector("tbody tr")
            # count the number of tables that contain these keywords
            for h in header:
                if "reales" in h.text or "Licencia" in h.text and "Licenciados" not in h.text:
                    count += 1
                    print(h.text)
            for h in header:
                if "reales" in h.text or "Licencia" in h.text and "Licenciados" not in h.text:
                    found += 1
                    rows = table.find_elements_by_css_selector("tbody tr")
                    country = ""
                    for row in rows:
                        tdata = row.find_elements_by_css_selector("td")
                        # First table found
                        if found == 1:
                            new_row = {}
                            if len(tdata) == 0:
                                continue
                            if len(tdata) == 1:
                                country = tdata[0].text
                            if len(tdata) == 3:
                                country = tdata[0].text
                                new_row = new_row = {'Region': country, 'Competicion': preprocess(tdata[1].text), 'Licencia': tdata[2].text}
                            if len(tdata) == 2:
                                new_row = new_row = {'Region': country, 'Competicion': preprocess(tdata[0].text), 'Licencia': tdata[1].text}
                            if new_row:
                                competiciones = competiciones.append(new_row, ignore_index=True)
                        # Second table found
                        if found == 2:
                            new_row2 = {}
                            print(row.text)
                            print(len(tdata))
                            if len(tdata) == 0:
                                continue
                            if len(tdata) == 3:
                                country = tdata[0].text
                            if len(tdata) == 1:
                                country = tdata[0].text
                            if len(tdata) == 2:
                                new_row2 = {'Region': country, 'Seleccion': preprocess(tdata[0].text), 'Licencia': tdata[1].text}
                            if new_row2 :
                                selecciones = selecciones.append(new_row2, ignore_index=True)
                    
        print(competiciones)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(selecciones)
    except NoSuchElementException:
        print("Cannot find table")