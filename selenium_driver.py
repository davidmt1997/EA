from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

# Custom Selenium driver class to manage calls to the Selenium framework
class Selenium_driver:

    '''
    Constructor where the path to the chromedriver is set
    '''
    def __init__(self, url):
        PATH = "/home/david/Dev/david/ea/EA/chromedriver_linux64/chromedriver"
        self.path = PATH
        self.url = url
        self.driver = None

    '''
    Function to connect the driver using the given options
    '''
    def connect_driver(self):
        # Using option headless to not see the window every time we scrape
        chrome_options = Options()  
        chrome_options.add_argument("--headless")

        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        chrome_options.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 1 
        })
        self.driver = webdriver.Chrome(executable_path=self.path,
                                    options=chrome_options)
        logging.info("Getting given URL")
        self.driver.get(self.url)
        return self.driver

    '''
    Custom function to disconnect the driver
    '''
    def diconnect_driver(self):
        logging.info("Diconnecting driver")
        self.driver.close()
