from selenium import webdriver
import os
from time import sleep
import time
import datetime

from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Helps us check for the presence of an element
from selenium.webdriver.common.by import By  # defines by what we are searching


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # need to create an instance of the below before being able to use them
        self.by = By
        self.ec = EC
        self.webDriverWait = WebDriverWait

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        service = webdriver.ChromeService(executable_path='C:/Users/user/PycharmProjects/InstaScraper/chromedriver.exe')
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login")

        username_field = self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.NAME, 'username')))  # we wait a maximum of 20 seconds while searching for the username bar which is tagged with 'username'
        username_field.send_keys(self.username)

        time.sleep(1)

        password_field = self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.NAME, 'password'))) # same for the password
        password_field.send_keys(self.password)

        time.sleep(1)

        log_in = self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))) # looks for login by using its Xpath (you can copy this from inspect)
        log_in.click()


    def get_css(self, text):
        return "." + ".".join(text.split())



    def get_following(self):
        self.driver.get(f"https://www.instagram.com/{self.username}/following/")
        time.sleep(5)
        element = "." + ".".join("_ap3a _aaco _aacw _aacx _aad7 _aade".split())
        followers_list = self.driver.find_element(By.CSS_SELECTOR, "._aano")

        for i in range(20):
            followers_list.send_keys(Keys.SPACE)
            time.sleep(0.5)

        elements = self.driver.find_elements(By.CSS_SELECTOR, self.get_css("x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1pi30zi x1swvt13 xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"))
        follower_dict = {}
        following_list = []

        # filters out suggested following
        for element in elements:
            following_button = element.find_element(By.CSS_SELECTOR, self.get_css("_ap3a _aaco _aacw _aad6 _aade"))
            following_element = element.find_element(By.CSS_SELECTOR, self.get_css("_ap3a _aaco _aacw _aacx _aad7 _aade"))
            following_button_text = following_button.get_attribute("innerHTML")
            if following_button_text == "Following":
                following_list.append(following_element)
            


        for follower in following_list:
            follower_name = follower.get_attribute("innerHTML")
            follower_link = f"https://www.instagram.com/{follower_name}/"
            if follower_name not in follower_dict:
                follower_dict[follower_name] = follower_link
        
        print(follower_dict)
        print(len(follower_dict))