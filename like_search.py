from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utility_methods.utility_methods import *
import urllib.request
import os


class InstaBot:

    def __init__(self, username=None, password=None):
        """"
        Creates an instance of InstaBot class.

        Args:
            username:str: The username of the user, if not specified, read from configuration.
            password:str: The password of the user, if not specified, read from configuration.

        Attributes:
            driver_path:str: Path to the chromedriver.exe
            driver:str: Instance of the Selenium Webdriver (chrome 72) 
            login_url:str: Url for logging into IG.
            nav_user_url:str: Url to go to a users homepage on IG.
            get_tag_url:str: Url to go to search for posts with a tag on IG.
            logged_in:bool: Boolean whether current user is logged in or not.
        """

        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']

        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']

        _browser_profile = webdriver.FirefoxProfile()
        _browser_profile.set_preference("dom.webnotifications.enabled", False)

        self.driver = webdriver.Firefox(firefox_profile=_browser_profile)

        self.logged_in = False


    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """

        self.driver.get(self.login_url)
        time.sleep(2)
        login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]') # login button xpath changes after text is entered, find first
        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        time.sleep(3)
        password_input.send_keys(Keys.RETURN)
        #login_btn.click()



    @insta_method
    def like_search(self, n_posts, like=True):
       
        action = 'Like' if like else 'Unlike'

        #close modal here
        #time.sleep(3)
        #self.driver.find_element_by_xpath("//*[text()='Turn On']").click()

        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[@aria-label='Find People']")))
        search.click()
        time.sleep(5)
      
        liked=0
        refresh = 0
        while True:
            time.sleep(10)
            image = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='react-root']/section/main/div/div[2]/div/div[1]/div[2]/div/a/div/div[2]")))
            image.click()
            j = 12
            while j > 0:
               try:
                   like = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='{}']".format(action))))
                   like.click()
                   print("liked")
                   time.sleep(3)
                   liked = liked + 1
                   nextbutton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']")))
                   nextbutton.click()
                   time.sleep(3)
               except:
                   print("Not liked")
                   nextbutton = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']")))
                   nextbutton.click()   
               j = j - 1
            self.driver.find_element_by_xpath("//*[@aria-label='Close']").click()  
            print("Total liked",liked)
            time.sleep(10)
            self.driver.refresh()
            refresh = refresh + 1
            print("refreshed", refresh, "times")





if __name__ == '__main__':

    config_file_path = './config.ini' 
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    bot = InstaBot()
    bot.login()

    bot.like_search( 100, like=True)
