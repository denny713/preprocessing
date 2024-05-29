import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#from webdriver_manager.chrome import ChromeDriverManager
import time

# other necessary ones
import urllib.request
from bs4 import BeautifulSoup as bs
import json
# import time
import re
import datetime

# FIXME: test multiple stuff

# Create browser
browser = webdriver.Chrome('')
browser.maximize_window()

# Credentials
EMAIL = "portgasd.fardan@yahoo.com"
PASSWORD = "Omah0354527581."

url = 'https://facebook.com'
# browser.get(url, 'Chrome', options=option)
browser.get(url)

# Login to facebook.com
wait = WebDriverWait(browser, 3600)
email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
email_field.send_keys(EMAIL)
pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
pass_field.send_keys(PASSWORD)
pass_field.send_keys(Keys.RETURN)

time.sleep(5)

# Open facebook and scroll down
browser.get(
    "https://www.facebook.com/Jokowi/posts/pfbid02PYB43WpgCQZxJUojPtAPEQ7T48WkfWx3VPUDTRRL1LFp1q8oUwxvggbeSw9s3mQnl")
time.sleep(10)
current_url = browser.current_url
split_url = current_url.split("/")
if split_url[4] != "posts":
    browser.quit()
    print("Video link, skip")

def change_type():
    select_type = browser.find_element(By.XPATH, "//span[contains(text(),'Paling Relevan')]")
    ActionChains(browser) \
        .move_to_element(select_type) \
        .click() \
        .perform()
    time.sleep(3)
    all_comments = browser.find_element(By.XPATH, "//span[contains(text(),'Semua Komentar')]")
    ActionChains(browser) \
        .move_to_element(all_comments) \
        .click() \
        .perform()
    time.sleep(3)


def view_more_comments():
    more_comments = browser.find_element(By.XPATH, "//span[contains(text(),'View more comments')]")
    ActionChains(browser) \
        .move_to_element(more_comments) \
        .click() \
        .perform()
    time.sleep(5)


def see_more():
    see_more_button = browser.find_elements(By.XPATH, "//div[contains(text(),'See more')]")
    for more in see_more_button:
        ActionChains(browser) \
            .move_to_element(more) \
            .click() \
            .perform()
        time.sleep(5)


def more_replies():
    more_replies_button = browser.find_elements(By.XPATH, "//span[contains(text(),'Replies')]")
    for more in more_replies_button:
        ActionChains(browser) \
            .move_to_element(more) \
            .click() \
            .perform()
        time.sleep(5)
    more_reply_button = browser.find_elements(By.XPATH, "//span[contains(text(),'Reply')]")
    for more in more_reply_button:
        ActionChains(browser) \
            .move_to_element(more) \
            .click() \
            .perform()
        time.sleep(5)


def scrap_comments():
    comments = browser.find_elements(By.XPATH, "//div[@dir='auto' and @style='text-align: start;']")
    comments_array = []
    for comment in comments:
        comments_array.append(comment.text)
        # time.sleep(5)
        with open('comments.txt', 'a', encoding='utf-8') as f:
            f.write(comment.text)
            f.write('\n')
    # print(comments_array)


# Program
change_type()

i = 0
while browser.find_element(By.XPATH, "//span[contains(text(),'View more comments')]").is_displayed() and i < 20:
    view_more_comments()
    i += 1

more_replies()
see_more()
scrap_comments()
