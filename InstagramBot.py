from selenium import webdriver
import os
from time import sleep
import time
import datetime
import pickle
import math

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

        followers_list = self.driver.find_element(By.CSS_SELECTOR, "._aano")
        following_number_elements = self.driver.find_elements(By.CSS_SELECTOR, self.get_css("html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"))

        following_number = int(following_number_elements[2].get_attribute("innerHTML"))
        time_to_scroll = math.ceil((following_number / 4) * 1.1)

        for i in range(int(time_to_scroll)):
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
            

        #initialises the following dictionary
        for follower in following_list:
            follower_name = follower.get_attribute("innerHTML")
            follower_link = f"https://www.instagram.com/{follower_name}/"
            if follower_name not in follower_dict:
                follower_dict[follower_name] = follower_link

        #Stores dictionary of following in seperate file 
        dict_file = open("following_dict.pkl", "wb")
        pickle.dump(follower_dict, dict_file)
        dict_file.close()




    def get_unfollowing(self, following_dict):
        unfollowing_list = []
        for following_name, following_link in following_dict.items():
            self.driver.get(f"{following_link}following/")

            search_bar = self.webDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.get_css('x1lugfcp x19g9edo x1lq5wgf xgqcy7u x30kzoy x9jhf4c x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x5n08af x5yr21d x1a2a7pz xyqdw3p x1pi30zi xg8j3zb x1swvt13 x1yc453h xh8yej3 xhtitgo xs3hnx8 xoy4bel x7xwk5j xvs91rp xp001vz'))))
            search_bar.send_keys(self.username)
            time.sleep(1)
            
            no_result = self.driver.find_elements(By.CSS_SELECTOR, self.get_css("x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj"))
            if len(no_result) != 0:
                unfollowing_list.append(following_name)
        
        return unfollowing_list
