# EA

This project consists on web scraping to extract information about EA games and their competitors. Load it into a database (Neo4j) and query to make visualizations.

To compare the FIFA 20 with eFootball PES 2020
* Web crawl to extract information about the games.
* Extract attributes (Developer, Publisher, Franchise, Genre, Platforms, Modes, Localized languages, launch date)
* Store attributes in graph database
* Query the database in order to make a visualization / info card comparison between the 2 games.

## Structure
This project is has some utility functions (the /scrappers files) used to extract data from Wikipedia, Steam, Facebook and Twitter.

The other files are class functions that help with the Selenium driver connectivity and the connections and pushes to the database.

## Prerequisites

* Having Python installed
* Having a running instance of an empty Neo4j database (preferably with a password that has to be entered in neo4j_graph.py)
* Creating a Twitter Developer account and filling the API keys in the scrapper/twitter_scrapper.py file
* Having a selenium Chrome driver in the project folder


## To run:

1. `git clone` or download the repo
2. make sure you have a driver for Selenium in the right path (if you are using Windows you will have to adjust the code to match the project PATH)
3. run `ṕip install -r requierements.txt`
4. run `python neo_push2.py`

## After running

The Neo4j Database will be populated with nodes and relationships (localhost:7474) that will be able to query and visualize in the browser.

To connect to a visualization tool such as Power BI: [Check this article here](https://xclave.co.uk/2019/02/06/actually-using-the-new-dataconnector-for-powerbi/)

Link to download the .mez file: [Here](https://github.com/cskardon/Neo4jDataConnectorForPowerBi/releases/tag/1.0.0)

After that, you can query the Neo4j DB from Power BI.
