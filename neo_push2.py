from scrappers.wiki_scrapper import get_game_title, get_info_table, get_scores_table
from scrappers.steam_scrapper import get_languages, get_realease_date
from scrappers.wiki_es_scrapper import get_commentaries, get_fifa_licenses_table, get_pes_licenses_table
from scrappers.twitter_scrapper import get_twitter_info
from scrappers.facebook_scrapper import get_fb_info
from selenium_driver import Selenium_driver
from neo4j_graph import Neo_Graph
import base64

class Neo_Push:

    # Create the graph instance
    def __init__(self):
        self.graph = Neo_Graph()
    
    '''
    Creates the in game language relationships from the dataframe received from the steam_scrapper
    Connects the given node with each language found on the table
    Arguments:
        df: Dataframe returned by the get_languages function
        node: language_node that connects the game_node with the language information
    '''
    def create_language_relationships_from_df(self, df, node):

        for i in df.itertuples():
            language = self.graph.create_node("Language", i[0])
            self.graph.create_relationship(node, "IN", language)

            if i[1] == 1:
                interface_node = self.graph.create_node("Interface", "Interface")
                self.graph.create_relationship(language, "HAS", interface_node)
            
            if i[2] == 1:
                audio_node = self.graph.create_node("Audio", "Full Audio")
                self.graph.create_relationship(language, "HAS", audio_node)
                
            if i[3] == 1:
                subtitle_node = self.graph.create_node("Subtitles", "Subtitle")
                self.graph.create_relationship(language, "HAS", subtitle_node)
                

    '''
    Creates the commentary relationships from the dataframe returned by the wiki_es_scrapper
    Matches the commentary node passed with the names of the commentarists using a language relationship
    Arguments:
        df: Dataframe returned by the get_commentaries function containing all the commentary information
        node: Commentary node, that connects with the game node and the commentarists names
    '''
    def create_commentary_relationships(self, df, node):
        
        for i in df.itertuples():
            commentarist = self.graph.create_node("Commentarist", i[3])
            self.graph.create_relationship(node, i[2], commentarist)

    '''
    Function to create the relationships of the National teams in FIfa
    Arguments:
        df: DataFrame containing all the relationships scraped
        node: national team node that connects with the game node
    '''
    def create_selecciones_relationships(self, df, node):
        for i in df.itertuples():
            country_node = self.graph.create_node("Country", i[1])
            self.graph.create_relationship(node, "COUNTRY", country_node)
            
            license_node = self.graph.create_node("License", i[2])
            self.graph.create_relationship(country_node, "LICENSED", license_node)
            
            if len(i) == 4:
                jugadores_reales_node = self.graph.create_node("Real_Players", i[3])
                self.graph.create_relationship(country_node, "REAL_PLAYERS", jugadores_reales_node)
                
    '''
    Function to create the relationships of the Competitions in Fifa
    Arguments:
        df: DataFrame containing all the relationships scraped
        node: competition node that connects with the game node
    '''
    def create_competiciones_relationships(self, df, node):
        competicion = df.iloc[0,0]
        competicion1 = df.Competicion.unique()[0]
        competicion2 = df.Competicion.unique()[1]
        competicion_node1 = self.graph.create_node("Competitions", competicion1)
        competicion_node2 = self.graph.create_node("Competitions", competicion2)
        
        for i in df.itertuples():
            if i[1] == competicion:
                self.graph.create_relationship(node, "COMPETITIONS", competicion_node1)
                
                country_node = self.graph.create_node("Country", i[2])
                self.graph.create_relationship(competicion_node1, "COUNTRY", country_node)
                
                item_node = self.graph.create_node("Item", i[3])
                self.graph.create_relationship(country_node, "ITEM", item_node)
                
                licencia_node = self.graph.create_node("License", i[4])
                self.graph.create_relationship(item_node, "LICENSED", licencia_node)
            else:
                self.graph.create_relationship(node, "COMPETITIONS", competicion_node2)
                
                country_node = self.graph.create_node("Country", i[2])
                self.graph.create_relationship(competicion_node2, "COUNTRY", country_node)
                
                item_node = self.graph.create_node("Item", i[3])
                self.graph.create_relationship(country_node, "ITEM", item_node)
                
                licencia_node = self.graph.create_node("License", i[4])
                self.graph.create_relationship(item_node, "LICENSED", licencia_node)
    
    '''
    Function to create the relationships of the Competitions in PES
    Arguments:
        df: DataFrame containing all the relationships scraped
        node: competition node that connects with the game node
    '''
    def create_pes_competiciones_relationships(self, df, node):
        for i in df.itertuples():
            if i[3] != "" and i[1] != "":
                country_node = self.graph.create_node("Country", i[1])
                self.graph.create_relationship(node, "COUNTRY", country_node)
                
                item_node = self.graph.create_node("Item", i[2])
                self.graph.create_relationship(country_node, "ITEM", item_node)
                
                name = ""
                if i[3] == "1":
                    name = "Sí"
                else:
                    name = "No"
                
                licencia_node = self.graph.create_node("License", name)
                self.graph.create_relationship(item_node, "LICENSED", licencia_node)

    '''
    Function to create the relationships of the National teams in PES
    Arguments:
        df: DataFrame containing all the relationships scraped
        node: national team node that connects with the game node
    ''' 
    def create_pes_selecciones_relationships(self, df, node):
        for i in df.itertuples():
            if i[3] != "":
                region_node = self.graph.create_node("Country", i[2])
                self.graph.create_relationship(node, "COUNTRY", region_node)
                
                if i[1] != "":
                    name = ""
                    if i[3] == "1":
                        name = "Sí"
                    else:
                        name = "No"

                    licencia_node = self.graph.create_node("License", name)
                    self.graph.create_relationship(region_node, "LICENSED", licencia_node)
                    
    '''
    Main function where all the data is retrieved and sent to the database
    Arguments:
        Array of urls
    '''
    def push(self, urls):
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
                    game_node = self.graph.create_node("Game", game)

                    print("Getting basic info table")
                    info = get_info_table(driver)
                    info_node = self.graph.create_node("Infos", "basic_info")

                    print("Getting scores table")
                    scores = get_scores_table(driver)
                    scores_node = self.graph.create_node("Scores", "scores")

                    # Insert game, info and scores into neo4j
                    self.graph.create_relationship(game_node, "HAS_INFO", info_node)
                    self.graph.create_relationship(game_node, "HAS_SCORES", scores_node)

                    for x, y in info.items():
                        i = self.graph.create_node("Info", y)
                        self.graph.create_relationship(info_node, x, i)

                    for x, y in scores.items():
                        for i in y:
                            iscore = self.graph.create_node("Score", i)
                            self.graph.create_relationship(scores_node, x, iscore)

                # Getting ES Wikipedia info
                elif "es.wikipedia" in url:
                    print("Getting commentaries table")
                    commentaries = get_commentaries(driver)
                    commentary_node = self.graph.create_node("Commentaries", "Commentaries")
                    self.graph.create_relationship(game_node, "HAS_COMMENTARIES", commentary_node)                        
                    self.create_commentary_relationships(commentaries, commentary_node)

                    print("Getting licenses tables")
                    license_node = self.graph.create_node("Licenses", "Licenses")
                    self.graph.create_relationship(game_node, "LICENSES", license_node)
                    
                    if "fifa" in url.lower():
                        competiciones, selec_masc, selec_fem = get_fifa_licenses_table(driver)
                        
                        selec_masc_node = self.graph.create_node("National_Teams", "Selecciones masculinas")
                        selec_fem_node = self.graph.create_node("National_Teams", "Selecciones femeninas")
                        self.graph.create_relationship(license_node, "NATIONAL_TEAMS", selec_masc_node)
                        self.graph.create_relationship(license_node, "NATIONAL_TEAMS", selec_fem_node)
                        
                        self.create_selecciones_relationships(selec_masc, selec_masc_node)
                        self.create_selecciones_relationships(selec_fem, selec_fem_node)
                        self.create_competiciones_relationships(competiciones, license_node)
                    else:
                        competiciones, selecciones = get_pes_licenses_table(driver)
                        competicion_node = self.graph.create_node("Competitions", "Competitions")
                        self.graph.create_relationship(license_node, "COMPETITIONS", competicion_node)
                        
                        seleccion_node = self.graph.create_node("National_Teams", "Selecciones")
                        self.graph.create_relationship(license_node, "NATIONAL_TEAMS", seleccion_node)
                        
                        self.create_pes_competiciones_relationships(competiciones, competicion_node)
                        self.create_pes_selecciones_relationships(selecciones, seleccion_node)
                
                # Getting steam data
                if "steampowered" in url:
                    print("Getting languages table")
                    languages = get_languages(driver)
                    language_node = self.graph.create_node("Languages", "languages")
                    self.graph.create_relationship(game_node, "HAS_LANGUAGES", language_node)
                    self.create_language_relationships_from_df(languages, language_node)
                    
                    print("Getting release date")
                    release_date = get_realease_date(driver)
                    release_node = self.graph.create_node("Date", release_date)
                    self.graph.create_relationship(game_node, "RELEASED", release_node)                        
                
                # Getting facebook data
                elif "facebook" in url:
                    print("Getting facebook data")
                    facebook_node = self.graph.create_node("SM", "facebook")
                    self.graph.create_relationship(game_node, "FB_DATA", facebook_node)
                    
                    likes, followers = get_fb_info(driver)
                    if likes != "":
                        fb_likes_node = self.graph.create_node("Likes", likes)
                        self.graph.create_relationship(facebook_node, "HAS_LIKES", fb_likes_node)
                        
                    if followers != "":
                        fb_followers_node = self.graph.create_node("Followers", followers)
                        self.graph.create_relationship(facebook_node, "HAS_FOLLOWERS", fb_followers_node)
                    
            
                # Disconnect from driver
                my_driver.diconnect_driver()
            
            # Getting Twitter data
            else:
                print("Getting twitter data")
                followers, rts_avg, fav_avg = get_twitter_info(url)
                twitter_node = self.graph.create_node("SM", "twitter")
                tw_followers_node = self.graph.create_node("Followers", followers)
                tw_rts_node = self.graph.create_node("Rts", rts_avg)
                tw_fav_node = self.graph.create_node("Fav", fav_avg)

                self.graph.create_node("Followers", followers)
                self.graph.create_node("Rts", rts_avg)
                self.graph.create_node("Favs", fav_avg)
                self.graph.create_relationship(game_node, "TW_DATA", twitter_node)
                self.graph.create_relationship(twitter_node, "HAS_FOLLOWERS", tw_followers_node)
                self.graph.create_relationship(twitter_node, "HAS_RETWEETS", tw_rts_node)
                self.graph.create_relationship(twitter_node, "HAS_FAVORITES", tw_fav_node)

        print("Done")

    def begin(self):
        self.graph.begin_transaction()

    def commit(self):
        self.graph.commit()

if __name__ == "__main__":
    # Steam is Fifa 21, can't find language for fifa 20
    FIFA_URLS = ["https://en.wikipedia.org/wiki/FIFA_20", "https://es.wikipedia.org/wiki/FIFA_20", "https://store.steampowered.com/app/1313860/EA_SPORTS_FIFA_21/", "https://www.facebook.com/easportsfifa", "EA"]
    PES_URLS = ["https://en.wikipedia.org/wiki/EFootball_PES_2020", "https://es.wikipedia.org/wiki/EFootball_Pro_Evolution_Soccer_2020", "https://store.steampowered.com/app/996470/eFootball__PES_2020/", "https://www.facebook.com/pes2020tr", "officialpes"]
    NHL_URLS = ["https://en.wikipedia.org/wiki/NHL_21"]				
    NFL_URLS = ["https://en.wikipedia.org/wiki/Madden_NFL_21", "https://store.steampowered.com/app/1239520/Madden_NFL_21/"]

    neo_push = Neo_Push()
    for urls in [FIFA_URLS, PES_URLS, NHL_URLS, NFL_URLS]:
        neo_push.begin()
        neo_push.push(urls)
        neo_push.commit()