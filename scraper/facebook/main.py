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

# Chrome options
# Options options = new Options()
# option = Options()
# option.add_argument("start-maximized")
# option.add_experimental_option("excludeSwitches", ["enable-logging"])
# option.add_argument("--disable-infobars")
# option.add_argument("--disable-extensions")

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# TODO: Add function to open multiple pages
# => Create loop for open page
# => Create Exception for the error which happen to the stuff
# ! FIXME: Create new stuff
# ? asfasf

print("===================================")
print("               MENU                ")
print("===================================")
print("1. Generate link and scrap")
print("2. Scrap from links.txt and compare with openedLinks.txt")
print("===================================")
print("Insert your choice (number): ")
user_choice = input()
print("User input = ", user_choice)

# Create browser
browser = webdriver.Chrome('')
# browser.maximize_window()

# Credentials
with open('credentials.txt') as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]

comments_added = [0]


# Commands

def scroll_to_bottom():
    loading_animation = browser.find_elements(By.XPATH, "//div[@role='progressbar' and @aria-valuetext='Loading...' and @data-visualcompletion='loading-state']")
    print("Locating loading bar")
    if len(loading_animation) > 0:
        for loading in loading_animation:
            try:
                print("Moving to the loading bar")
                ActionChains(browser) \
                    .move_to_element(loading) \
                    .pause(15) \
                    .perform()
                time.sleep(5)
            except:
                try:
                    browser.execute_script("arguments[0].click();", type) 
                except:
                    continue
    else:
        pass


def back_to_top():
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")  # scroll back to the top
    time.sleep(10)


# FOR SCRAPING COMMENTS
# Commands
def change_type():
    select_type = browser.find_elements(By.XPATH, "//span[contains(text(),'Most relevant')]")
    print("Finding selection")
    if len(select_type) > 0:
        for stype in select_type:
            try:
                ActionChains(browser) \
                    .move_to_element(stype) \
                    .pause(2) \
                    .click() \
                    .perform()
                time.sleep(2)
                print("Moving to the selection")
            except:
                try:
                    browser.execute_script("arguments[0].click();", stype)
                except:
                    continue
        all_comments = browser.find_elements(By.XPATH, "//span[contains(text(),'All comments')]")
        if len(all_comments) > 0:
            for all_comment in all_comments:
                try:
                    ActionChains(browser) \
                        .move_to_element(all_comment) \
                        .pause(2) \
                        .click() \
                        .perform()
                    time.sleep(1)
                    print("Selecting the All Comments")
                    print(select_type.text)
                except:
                    try:
                        browser.execute_script("arguments[0].click();", all_comment)
                    except:
                        continue
        else:
            pass
    else:
        pass


def view_more_comments():
    more_comments = browser.find_elements(By.XPATH, "//span[contains(text(),'View more comments')]")
    time.sleep(1)
    if len(more_comments) > 0:
        for more_comment in more_comments:
            try:
                ActionChains(browser) \
                    .move_to_element(more_comment) \
                    .pause(2) \
                    .click() \
                    .perform()
                # time.sleep(1)
            except:
                try:
                    browser.execute_script("arguments[0].click();", more_comment)
                except:
                    continue
    else:
        pass


def see_more():
    see_more_button = browser.find_elements(By.XPATH, "//div[contains(text(),'See more')]")
    time.sleep(2)
    if len(see_more_button) > 0:
        for more in see_more_button:
            try:
                ActionChains(browser) \
                    .move_to_element(more) \
                    .pause(2) \
                    .click() \
                    .perform()
                time.sleep(2)
            except:
                try:
                    browser.execute_script("arguments[0].click();", more)
                except:
                    continue
    else:
        pass


def more_replies():
    more_replies_button = browser.find_elements(By.XPATH, "//span[contains(text(),'Replies')]")
    time.sleep(2)
    if len(more_replies_button) > 0:
        for replies in more_replies_button:
            try:
                ActionChains(browser) \
                    .move_to_element(replies) \
                    .pause(2) \
                    .click() \
                    .perform()
                time.sleep(2)
            except:
                try:
                    browser.execute_script("arguments[0].click();", replies)
                except:
                    continue
    else:
        pass
    more_reply_button = browser.find_elements(By.XPATH, "//span[contains(text(),'Reply')]")
    time.sleep(2)
    if len(more_reply_button) > 0:
        for reply in more_reply_button:
            try:
                ActionChains(browser) \
                    .move_to_element(reply) \
                    .pause(2) \
                    .click() \
                    .perform()
                time.sleep(2)
            except:
                try:
                    browser.execute_script("arguments[0].click();", reply)
                except:
                    continue
    else:
        pass


def scrap_comments(added=comments_added[0]):
    comments = browser.find_elements(By.XPATH, "//div[@dir='auto' and @style='text-align: start;']")
    time.sleep(3)
    if len(comments) > 0:
        time.sleep(3)
        # comments_array = []
        for comment in comments:
            # comments_array.append(comment.text)
            # time.sleep(5)
            print("Comments added :", added)
            added += 1
            with open('comments.txt', 'a', encoding='utf-8') as f:
                f.write(comment.text)
                f.write('\n')
    else:
        pass
    comments_added[0] += added - 1
    print("Total added :", comments_added[0])


# browser.get(URL, 'Chrome', options=option)
browser.get('https://facebook.com')

# Login to facebook.com
wait = WebDriverWait(browser, 3600)
email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
email_field.send_keys(EMAIL)
pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
pass_field.send_keys(PASSWORD)
pass_field.send_keys(Keys.RETURN)
print("Successfully login")

time.sleep(5)

listLinks = []
if user_choice == '1':
    # Open facebook page and scroll down
    URL = 'https://web.facebook.com/SBYudhoyono'
    browser.get(URL)
    print("Opening page")
    time.sleep(10)

    i = 0
    while i < 50:
        scroll_to_bottom()
        i += 1
        print("Scrolling", i, "times")

    time.sleep(5)
    back_to_top()
    time.sleep(5)

    # FOR SCRAPPING POSTS
    # Find post links
    postLinks = browser.find_elements(By.XPATH,
                                      "//div[@class='g4tp4svg mfclru0v om3e55n1 p8bdhjjv']//a[@class='qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq jxuftiz4 cxfqmxzd tes86rjd']")

    # Move to each post link so the link appear and get the href attribute

    index = 0
    for postLink in postLinks:
        print("Getting link", index)
        # print(postLink)
        time.sleep(10)
        try:
            ActionChains(browser) \
                .move_to_element(postLink) \
                .perform()
            time.sleep(15)
            link = postLink.get_attribute('href')
            listLinks.append(link)
            print("Link added", index, link)
            with open('links.txt', 'a', encoding='utf-8') as f:
                f.write(link)
                f.write('\n')
            index += 1
        except:
            pass
elif user_choice == '2':
    # Using readlines
    print("In 2")
    links = open('links.txt', 'r')
    listLinks = links.readlines()

# print("Links :", listLinks)
# print("Total Links", len(listLinks))

index = 0
for link in listLinks:
    links = open('openedLinks.txt', 'r')
    openedLinks = links.readlines()
    if link not in openedLinks:
        browser.get(link)
        print("Opening link", index)
        with open('openedLinks.txt', 'a', encoding='utf-8') as f:
            f.write(link.strip())
            f.write('\n')
        index += 1
        time.sleep(5)
        current_url = browser.current_url
        split_url = current_url.split("/")
        if split_url[4] == "posts":
            # Program
            change_type()
            print("Changing comment selection")

            i = 0
            j = 0
            while i < 50:
                i += 1
                if browser.find_elements(By.XPATH, "//span[contains(text(),'View more comments')]"):
                    view_more_comments()
                    print("Viewing more comments")
                elif j == 3:
                    print("No more comments")
                    break
                else:
                    j += 1

            print("Opening replies")
            more_replies()
            time.sleep(2)
            print("Expanding comments")
            see_more()
            time.sleep(2)
            print("Scraping comments")
            scrap_comments()
            time.sleep(2)
