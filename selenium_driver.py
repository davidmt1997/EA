from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

# Custom Selenium driver class to manage calls to the Selenium framework
class Selenium_driver:
    def __init__(self, url):
        PATH = "/home/david/Dev/david/ea/EA/chromedriver_linux64/chromedriver"
        self.path = PATH
        self.url = url
        self.driver = None

    def connect_driver(self):
        # Using option headless to not see the window every time we scrape
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        self.driver = webdriver.Chrome(executable_path=self.path,
                                    options=chrome_options)
        logging.info("Getting given URL")
        self.driver.get(self.url)
        return self.driver

    def diconnect_driver(self):
        logging.info("Diconnecting driver")
        self.driver.close()
