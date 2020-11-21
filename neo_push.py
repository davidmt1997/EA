from py2neo import Graph, Node, Relationship
from wiki_scrapper import get_game_title, get_info_table, get_scores_table
from steam_scrapper import get_languages, get_realease_date
from wiki_es_scrapper import get_commentaries, get_fifa_licenses_table, get_pes_licenses_table
from twitter_scrapper import get_twitter_info
from facebook_scrapper import get_fb_info
import logging
from selenium_driver import Selenium_driver

graph = Graph(password="03111997")

# Steam is Fifa 21, can't find language for fifa 20
FIFA_URLS = ["https://en.wikipedia.org/wiki/FIFA_20", "https://es.wikipedia.org/wiki/FIFA_20", "https://store.steampowered.com/app/1313860/EA_SPORTS_FIFA_21/", "https://www.facebook.com/easportsfifa", "EA"]
PES_URLS = ["https://en.wikipedia.org/wiki/EFootball_PES_2020", "https://es.wikipedia.org/wiki/EFootball_Pro_Evolution_Soccer_2020", "https://store.steampowered.com/app/996470/eFootball__PES_2020/", "https://www.facebook.com/pes2020tr", "officialpes"]
NHL_URLS = ["https://en.wikipedia.org/wiki/NHL_21"]				
NFL_URLS = ["https://en.wikipedia.org/wiki/Madden_NFL_21", "https://store.steampowered.com/app/1239520/Madden_NFL_21/"]

tx = graph.begin()

def create_language_relationships_from_df(df, node):
	for i in df.itertuples():
		language = Node("Language", name=i[0])
		rel = Relationship(node, "IN", language)
		tx.create(rel)
		if i[1] == 1:
			interface_node = Node("Interface", name="Interface")
			rel = Relationship(language, "HAS", interface_node)
			tx.create(rel)
		if i[2] == 1:
			audio_node = Node("Audio", name="Full Audio")
			rel = Relationship(language, "HAS", audio_node)
			tx.create(rel)
		if i[3] == 1:
			subtitle_node = Node("Subtitles", name="Subtitle")
			rel = Relationship(language, "HAS", subtitle_node)
			tx.create(rel)

def create_commentary_relationships(df, node):
	for i in df.itertuples():
		commentarist = Node("Commentarist", name=i[3])
		rel = Relationship(node, i[2], commentarist)
		tx.create(rel)

def create_selecciones_relationships(df, node):
	for i in df.itertuples():
		country_node = Node("Country", name=i[1])
		rel = Relationship(node, "country", country_node)
		tx.create(rel)
		license_node = Node("Licencia", name=i[2])
		rel = Relationship(country_node, "licenciada", license_node)
		tx.create(rel)
		if len(i) == 4:
			jugadores_reales_node = Node("Reales", name=i[3])
			rel = Relationship(country_node, "jugadores reales", jugadores_reales_node)
			tx.create(rel)

def create_competiciones_relationships(df, node):
	competicion = df.iloc[0,0]
	competicion1 = df.Competicion.unique()[0]
	competicion2 = df.Competicion.unique()[1]
	competicion_node1 = Node("Competiciones", name=competicion1)
	competicion_node2 = Node("Competiciones", name=competicion2)
	for i in df.itertuples():
		if i[1] == competicion:
			rel = Relationship(node, "competiciones", competicion_node1)
			tx.create(rel)
			country_node = Node("Country", name=i[2])
			rel = Relationship(competicion_node1, "country", country_node)
			tx.create(rel)
			item_node = Node("Item", name=i[3])
			rel = Relationship(country_node, "item", item_node)
			tx.create(rel)
			licencia_node = Node("Licencia", name=i[4])
			rel = Relationship(item_node, "licenciada", licencia_node)
			tx.create(rel)
		else:
			rel = Relationship(node, "competiciones", competicion_node2)
			tx.create(rel)
			country_node = Node("Country", name=i[2])
			rel = Relationship(competicion_node2, "country", country_node)
			tx.create(rel)
			item_node = Node("Item", name=i[3])
			rel = Relationship(country_node, "item", item_node)
			tx.create(rel)
			licencia_node = Node("Licencia", name=i[4])
			rel = Relationship(item_node, "licenciada", licencia_node)
			tx.create(rel)

def create_pes_competiciones_relationships(df, node):
	for i in df.itertuples():
		if i[3] != "" and i[1] != "":
			country_node = Node("Country", name=i[1])
			rel = Relationship(node, "country", country_node)
			tx.create(rel)
			item_node = Node("Item", name=i[2])
			rel = Relationship(country_node, "item", item_node)
			tx.create(rel)
			name = ""
			if i[3] == "1":
				name = "Sí"
			else:
				name = "No"
			licencia_node = Node("Licencia", name=name)
			rel = Relationship(item_node, "licenciada", licencia_node)
			tx.create(rel)
	

def create_pes_selecciones_relationships(df, node):
	for i in df.itertuples():
		if i[3] != "":
			region_node = Node("Country", name=i[2])
			rel = Relationship(node, "country", region_node)
			tx.create(rel)
			if i[1] != "":
				name = ""
				if i[3] == "1":
					name = "Sí"
				else:
					name = "No"
				licencia_node = Node("Licencia", name=name)
				rel = Relationship(region_node, "licenciada", licencia_node)
				tx.create(rel)

def main():
	for urls in [FIFA_URLS, PES_URLS, NHL_URLS, NFL_URLS]:
		for url in urls:

			# If https in url, retrieving data using Selenium
			# Create driver and connect to url
			if "https" in url:
				my_driver = Selenium_driver(url)
				driver = my_driver.connect_driver()
				
				# Getting en Wikipedia info
				if "en.wikipedia" in url:
					print("Getting game title")
					game = get_game_title(driver)
					game_node = Node("Game", name=game)

					print("Getting basic info table")
					info = get_info_table(driver)
					info_node = Node("Infos", name="basic_info")

					print("Getting scores table")
					scores = get_scores_table(driver)
					scores_node = Node("Scores", name="scores")
					# Insert game, info and scores into neo4j
					
					r1 = Relationship(game_node, "HAS_INFO", info_node)
					tx.create(r1)
					r2 = Relationship(game_node, "HAS_SCORES", scores_node)
					tx.create(r2)

					for x, y in info.items():
						i = Node("Info", name=y)
						rel = Relationship(info_node, x, i)
						tx.create(rel)

					for x, y in scores.items():
						for i in y:
							iscore = Node("Score", name=i)
							rel = Relationship(scores_node, x, iscore)
							tx.create(rel)

				# Getting es Wikipedia info
				elif "es.wikipedia" in url:
					print("Getting commentaries table")
					commentaries = get_commentaries(driver)
					commentary_node = Node("Commentaries", name="commentaries")
					
					rel = Relationship(game_node, "HAS_COMMENTARIES", commentary_node)
					tx.create(rel)
					create_commentary_relationships(commentaries, commentary_node)
					print("Getting licenses tables")
					license_node = Node("Licencias", name="Licencias")
					rel = Relationship(game_node, "licenses", license_node)
					tx.create(rel)
					if "fifa" in url.lower():
						competiciones, selec_masc, selec_fem = get_fifa_licenses_table(driver)
						
						selec_masc_node = Node("Selecciones", name="selecciones masculinas")
						selec_fem_node = Node("Selecciones", name="selecciones femeninas")
						rel = Relationship(license_node, "selecciones", selec_masc_node)
						tx.create(rel)
						rel = Relationship(license_node, "selecciones", selec_fem_node)
						tx.create(rel)
						create_selecciones_relationships(selec_masc, selec_masc_node)
						create_selecciones_relationships(selec_fem, selec_fem_node)
						create_competiciones_relationships(competiciones, license_node)
					else:
						competiciones, selecciones = get_pes_licenses_table(driver)
						competicion_node = Node("Competiciones", name="competiciones")
						rel = Relationship(license_node, "competiciones", competicion_node)
						tx.create(rel)
						seleccion_node = Node("Selecciones", name="selecciones")
						rel = Relationship(license_node, "selecciones", seleccion_node)
						tx.create(rel)
						create_pes_competiciones_relationships(competiciones, competicion_node)
						create_pes_selecciones_relationships(selecciones, seleccion_node)
				
				# Getting steam data
				if "steampowered" in url:
					print("Getting languages table")
					languages = get_languages(driver)
					language_node = Node("Languages", name="languages")
					
					rel = Relationship(game_node, "HAS_LANGUAGES", language_node)
					tx.create(rel)
					create_language_relationships_from_df(languages, language_node)
					
					print("Getting release date")
					release_date = get_realease_date(driver)
					release_node = Node("Date", name=release_date)
					r = Relationship(game_node, "RELEASED", release_node)
					tx.create(r)
					
				
				# Getting facebook data
				elif "facebook" in url:
					print("Getting facebook data")
					facebook_node = Node("SM", name="facebook")
					rel = Relationship(game_node, "FB_DATA", facebook_node)
					tx.create(rel)
					likes, followers = get_fb_info(driver)
					if likes != "":
						fb_likes_node = Node("Likes", name=likes)
						r3 = Relationship(facebook_node, "HAS_LIKES", fb_likes_node)
						tx.create(r3)
					if followers != "":
						fb_followers_node = Node("Followers", name=followers)
						r4 = Relationship(facebook_node, "HAS_FOLLOWERS", fb_followers_node)
						tx.create(r4)
					
			
				# Disconnect from driver
				my_driver.diconnect_driver()
			
			# Getting Twitter data
			else:
				print("Getting twitter data")
				followers, rts_avg, fav_avg = get_twitter_info(url)
				twitter_node = Node("SM", name="twitter")
				tw_followers_node = Node("Followers", name=followers)
				tw_rts_node = Node("Rts", name=rts_avg)
				tw_fav_node = Node("Fav", name=fav_avg)
				rel = Relationship(game_node, "TW_DATA", twitter_node)
				tx.create(rel)
				r3 = Relationship(twitter_node, "HAS_FOLLOWERS", tw_followers_node)
				tx.create(r3)
				r4 = Relationship(twitter_node, "HAS_RETWEETS", tw_rts_node)
				tx.create(r4)
				r5 = Relationship(twitter_node, "HAS_FAVORITES", tw_fav_node)
				tx.create(r5)

	tx.commit()
	print("Done")

if __name__ == "__main__":
	main()
