#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
import time
driver = webdriver.Chrome('')
driver.maximize_window()
driver.get("https://instagram.com/")

# In[ ]:


# Select the password & username
username=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
password=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))

username.clear()
password.clear()

#Insert login info 
#Please Enter your account for the script to run 
username.send_keys("suka.enelpe@gmail.com")
password.send_keys("Sukanlp123.")


# In[ ]:


#login
login=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()    

# In[ ]:


# pass the first 2 pop ups after the login
#not_now1 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Not Now')]"))).click()
not_now_button1 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37'][contains(text(),'Not now')]")))
not_now_button1.click()
#not_now2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
not_now_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_a9-- _ap36 _a9_1' and text()='Not Now']")))
not_now_button2.click()

# In[ ]:


#Activate the searchbox
elements = driver.find_elements(By.CSS_SELECTOR,"div[class='x1n2onr6']")
no=0
for element in elements:
    if(no == 2):
        element.click()
    no +=1
    

#Select the searchbox
searchbox=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Search']"))) 

searchbox.clear()

keyword="#pilpres2024"

#search for the keyword
searchbox.send_keys(keyword)

# Wait for 5 seconds
time.sleep(5) 

#Enter to the keyword content 
key_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
key_link.click()

# In[ ]:


#searchbox.send_keys(Keys.ENTER)

# In[ ]:


last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page 
    time.sleep(10)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# In[ ]:


#target all the link elements on the page
post_links = driver.find_elements(By.TAG_NAME, "a")
post_links = [a.get_attribute('href') for a in post_links]

#narrow down all links to image links only
post_links = [a for a in post_links if str(a).startswith("https://www.instagram.com/p/")]

print('Found ' + str(len(post_links)) + ' links to images')
post_links[:5]

# In[ ]:


from selenium.common.exceptions import TimeoutException
def tap(wait,xpath):
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    

# In[ ]:


images = []
data=[]
wait = WebDriverWait(driver, 1)
i=0
#Follow each post link to all post images, text, and comments
for link in post_links[:5]:
    driver.get(link)
    #time.sleep(5)
    #Tap until the end to open all collapsed elements
    while True:
        try:
           tap(wait,"//button[class='_acan _acao _acas']")
           tap(wait,"//button[class='_abl']")    
        except TimeoutException:
            break
    #Tap until the end to get all images
    while True:
        try:
            
            img=driver.find_elements(By.XPATH, "//div[@class='_aagu _aato']//img")
            img = [i.get_attribute('src') for i in img]
            tap(wait,"//button[@aria-label='Next']")
        except TimeoutException:
            break
    img = list(dict.fromkeys(img))    
    print(type(img))
    #text= driver.find_elements(By.XPATH, "div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']")
    text= driver.find_elements(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']//span[text()]")
    text = [t.text for t in text]
    
    # no=0
    # array_comment = []
    # for element in text:
    #     array_element = element.text
    #     print(array_element)
    #     text_element = array_element
    #     if(no == 2):
    #         array_comment.append(text_element)
    #     no +=1
    #print(text[0])
    
    time = driver.find_elements(By.XPATH, "//time[@class='x1ejq31n xd10rxx x1sy0etr x17r0tee x1roi4f4 xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6']")
    times = [t.get_attribute('datetime') for t in time]
    
    #print(len(img))
    #post={"_id": i,"post_link":link,"comments":text[1:]}
    post={"_id": i,
          "post_link":link,
          "comments":text, 
          "time":times}
    #post={"_id": i,"post_link":link,"comments":array_comment}
    print(post)
    i=i+1
    data.append(post)
   
      

# In[ ]:


print(data)

# In[ ]:


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

# In[ ]:


client.stats 

# In[ ]:


instagram_comments_db = client['instagram_comments_db']
comments_collection = instagram_comments_db['comments_collection']
comments_collection.insert_many(data)
