#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

# In[2]:


# Create browser
#browser = webdriver.Chrome('')
#browser.maximize_window()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()

EMAIL = "suka.enelpe@gmail.com"
PASSWORD = "Sukanlp123."

url = 'https://facebook.com'
# browser.get(url, 'Chrome', options=option)
browser.get(url)

# In[3]:


# Login to facebook.com
wait = WebDriverWait(browser, 3600)
email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
email_field.send_keys(EMAIL)
pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
pass_field.send_keys(PASSWORD)
pass_field.send_keys(Keys.RETURN)

time.sleep(5)

# In[4]:


# Open facebook and scroll down
browser.get(
    "https://www.facebook.com/Jokowi/posts/pfbid02jgR76SqznUiUj9SXTSFpS9756AdStUug1VPnbgguG5ALrMm3VeUzSjhRuyGRzr2il")
time.sleep(10)

# Simpan hasil scrap dalam bentuk list
scraped_data = []

# Fungsi untuk menampilkan komentar ke konsol dengan XPath
def display_comments():
    try:
        # Tunggu beberapa detik untuk memastikan halaman sudah dimuat sepenuhnya
        time.sleep(5)
        
        # Loop untuk mengklik "Lihat komentar lain" beberapa kali
        for _ in range(2):  # Ganti angka ini sesuai kebutuhan
            # Temukan elemen "Lihat komentar lain" dan klik
            view_more_comments_button = browser.find_element(By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa' and @dir='auto' and text()='Lihat komentar lain']")
            view_more_comments_button.click()
            time.sleep(5)  # Tunggu beberapa detik setelah mengklik

        # Temukan elemen-elemen yang berisi komentar dengan XPath
        comments = browser.find_elements(By.XPATH, "//div[@class='x1y1aw1k xn6708d xwib8y2 x1ye3gou']")

        # Loop melalui elemen-elemen komentar dan tambahkan ke list
        for comment in comments:
            # Ambil teks komentar
            comment_text = comment.find_element(By.XPATH, ".//div[@dir='auto' and @style='text-align: start;']").text
           
            # Tambahkan data ke list
            scraped_data.append({"comment": comment_text})

        # Simpan list dalam file JSON
        with open(r"C:\Users\tsaqi\Documents\Scraper\Fardan\Tugas Scrapper KCI Sosmed\hasil_scrap_FB.json", "w", encoding="utf-8") as json_file:
            json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)
        
        print("Scraping selesai. Hasil disimpan dalam file JSON.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Panggil fungsi
display_comments()


# In[5]:


import pymongo
from pymongo import MongoClient
import certifi

ca = certifi.where()

user = 'scraper-sosmed'
sandi = '0354527581'
# uri (uniform resource identifier) defines the connection parameters

uri = 'mongodb+srv://'+ user +':'+ sandi +'@scraper.ychmtel.mongodb.net/?retryWrites=true&w=majority'
# start client to connect to MongoDB server
client = MongoClient(uri, tlsCAFile=ca)

# In[6]:


client.stats 

# In[7]:


facebook_comments_db = client['facebook_comments_db']
comments_collection = facebook_comments_db['comments_collection']
comments_collection.insert_many(scraped_data)

# In[ ]:



