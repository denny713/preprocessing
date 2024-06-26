#!/usr/bin/env python
# coding: utf-8

# In[13]:


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from urllib.parse import quote
import time

# In[4]:


opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox') #Disables the sandbox for all process types that are normally sandboxed. Meant to be used as a browser-level switch for testing purposes only. 
# opt.add_argument('--headless') #Run in headless mode, i.e., without a UI or display server dependencies. 
opt.add_argument('--disable-notifications')#Disables the Web Notification and the Push APIs.
opt.add_argument('--disable-gpu')
opt.add_argument('--disable-3d-apis')  #Disables warning GPU stall

driver = webdriver.Chrome(options=opt)#setting up webdriver and option


# In[2]:


judul_buku = 'daun'
judul_buku = quote(judul_buku)
url = 'https://www.goodreads.com/search?utf8=%E2%9C%93&search_type=books&q=' + judul_buku
content = driver.get(url) #target website

last_height = driver.execute_script("return document.body.scrollHeight")

SCROLL_PAUSE_TIME = 5 #detik

while True:
    # Scroll down to bottom
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollBy(0, 800);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(SCROLL_PAUSE_TIME)
content_items = driver.find_elements(By.XPATH, "//table[@class='tableList']")

if len(content_items)>0:
    isi_tabel = content_items[0].get_attribute('innerHTML')
    # print('isi tabel: ' + isi_tabel)
    daftar_buku = content_items[0].find_elements(By.XPATH, "//tr")
    if len(daftar_buku)>0:
        buku_list = []
        for buku in daftar_buku:
            # detail_buku = buku.get_attribute('innerHTML')
            # print(detail_buku)

            link_buku = buku.find_elements(By.XPATH, "//a[@class='bookTitle']")
            if len(link_buku)>0:
                str_link_buku = link_buku[0].get_attribute('href')
            else:
                str_link_buku = ''

            judul_buku = buku.find_elements(By.XPATH, "//span[@itemprop='name']")
            if len(judul_buku)>0:
                str_judul_buku = judul_buku[0].text
            else:
                str_judul_buku = ''

            buku = {
                "judul" : str_judul_buku,
                "link" : str_link_buku
            }

            buku_list.append(buku)

        print(str(buku_list))
        
driver.close()

# In[ ]:




# In[ ]:



