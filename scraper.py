from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from time import sleep
#import json
import random
import os
import config
import urllib.request


class Scraper:
    def __init__(self):
        self.profile_url = config.profile_url
        self.PATH = config.chromedriver_path
        
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(self.PATH, options = self.options)

        self.browser_session = None

        #self.browser_visit = 0

        #self.login = 0

        # delay in seconds
        self.interval = 5

        self.user = config.login_username
        
        self.password = config.login_pass

        #self.photo_link = None

        self.image_links = []


    def initiate_chrome(self):
        if self.browser_session == None:
            self.browser_session =  self.driver
            return 1
        else:
            return 0

    def close_chrome(self):
    	if self.browser_session == None:
    		return 1
    	else:
    		self.browser_session.close()
    		self.browser_session.quit()
    		self.browser_session = None
    		return 1

    def facebook_login(self):
        self.driver.get("https://www.facebook.com/")
        print("Opened Facebook.com")
        sleep(1)

        if (self.user == None and self.password == None):
            self.user = input("Enter Email: ")
            self.password = input("Enter Password: ")

        username_box =  self.driver.find_element_by_id("email")
        username_box.send_keys(self.user)
        print ("Email entered")
        sleep(1)

        password_box = self.driver.find_element_by_id("pass")
        password_box.send_keys(self.password)
        print("Password entered")

        login_box =  self.driver.find_element_by_name("login")
        login_box.click()
        print("sleeping for 15 seconds")
        time.sleep(15)
        print("Login Attempted hopefully successful")

    def scroll_down(self):
        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_photos_by(self):
        if (self.profile_url == None):
            print("Example: https://www.facebook.com/Nintendo")
            self.profile_url = input("Enter a profile url: ")
        if ("=id" in self.profile_url):
            self.driver.get(self.profile_url + "&sk=photos_by")
        else:
            self.driver.get(self.profile_url + "photos_by")
        print("Opened /photos_by")
        sleep(random.uniform(7, 10))
        self.scroll_down()
        print("Scrolled Down")
        #links = self.driver.find_elements_by_tag_name("a")
        links = self.driver.find_elements_by_tag_name('a')
        links = [i.get_attribute('href') for i in links]
        links = [i for i in links if "photo" in str(i)]
        for i in range(len(links)):
            if self.profile_url in str(links[i]):
                links.pop(i)
                break
        print("Discovered " + str((len(links))) + "images")
        with open("links.txt", 'w') as f:
            for i in links:
                f.write(str(i) + "\n")
        for i in links:
            self.driver.get(i)
            sleep(random.uniform(5, 7))
            image_link = self.driver.find_element_by_class_name("r0294ipz")
            time.sleep(0.5)
            image_link = image_link.get_attribute("src")
            self.image_links.append(image_link)
        sleep(random.uniform(2,3))
        
    def write_to_txt(self):
        with open("output.txt", 'w') as f:
            for i in self.image_links:
                f.write(str(i) + "\n")

    def download_all(self):
        count = 1
        for line in self.image_links:
            print("Downloading image " + str(count))
            response = urllib.request.urlopen(line)
            time.sleep(1)
            with open(str(count) + ".png", "wb") as f:
                f.write(response.read())
            count += 1

    def download_from_file(self):
        count = 1
        file_obj = open("output.txt", 'r')
        lines = file_obj.readlines()
        for line in lines:
            print("Downloading image " + str(count))
            response = urllib.request.urlopen(line)
            time.sleep(1)
            with open(str(count) + ".png", "wb") as f:
                f.write(response.read())
            count += 1

def main():
    facebook = Scraper()
    #facebook.initiate_chrome()
    facebook.facebook_login()
    facebook.get_photos_by()
    facebook.write_to_txt()
    facebook.download_all()
    #facebook.download_from_file()

if __name__ == "__main__":
    print("Scraper is on")
    main()