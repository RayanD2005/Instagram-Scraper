from selenium import webdriver
import os
from time import sleep
import time
import datetime
from InstagramBot import InstagramBot

from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Helps us check for the presence of an element
from selenium.webdriver.common.by import By  # defines by what we are searching

"""
username = input(print("Username: "))
username = username.strip()
password = input(print("Password: "))
password = password.strip()
"""
ig = InstagramBot("rdtester21", "cranking90s") # an instagram account created for the sole purpose of testing this
time.sleep(1)  # use sleep to wait for a page to load before running scripts on the page
ig.login()
time.sleep(5)
ig.get_following()


