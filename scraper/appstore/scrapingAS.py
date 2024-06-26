#!/usr/bin/env python
# coding: utf-8

# In[1]:


!pip install app-store-scraper
!pip install itunes-app-scraper-dmi
!pip install pymongo[srv]

# In[2]:


import pandas as pd

# for scraping app info from App Store
from itunes_app_scraper.scraper import AppStoreScraper

# for scraping app reviews from App Store
from app_store_scraper import AppStore

# for pretty printing data structures
from pprint import pprint

# for keeping track of timing
import datetime as dt
from tzlocal import get_localzone

# for building in wait times
import random
import time

## Set up loop to go through all apps
import os

# In[3]:


# from google.colab import drive
# drive.mount('/content/drive')

# In[4]:


import datetime                            # Imports datetime library

import pymongo
from pymongo import MongoClient

user = 'alfalimbany'
sandi = 'BangRaf454647'
# uri (uniform resource identifier) defines the connection parameters

uri = 'mongodb+srv://'+ user +':'+ sandi +'@kuliah.uohhxud.mongodb.net/?retryWrites=true&w=majority'
# start client to connect to MongoDB server
client = MongoClient(uri)

# In[ ]:


client.stats                                # .stats  show details about the client

# In[ ]:


App_store_db = client['App_store_db']

info_collection = App_store_db['info_collection']

comment_collection = App_store_db['comment_collection']

# In[ ]:


## Read in file containing app names and IDs
app_df = pd.read_csv('/content/drive/MyDrive/Kuliah/RPL/scraper/AppStore/apps.csv')
app_df.head()

# In[ ]:


## Get list of app names and app IDs
app_names = list(app_df['iOS_app_name'])
app_ids = list(app_df['iOS_app_id'])

# In[ ]:


## Set up App Store Scraper
scraper = AppStoreScraper()
app_store_list = list(scraper.get_multiple_app_details(app_ids))

## Pretty print the data for the first app
pprint(app_store_list[0])

# In[ ]:


## Convert list of dicts to Pandas DataFrame and write to csv
app_info_df = pd.DataFrame(app_store_list)
info_collection.insert_many(app_store_list) #MongoDB
app_info_df.to_csv('/content/drive/MyDrive/Kuliah/RPL/scraper/AppStore/appsDetail.csv', index=False) #CSV
app_info_df.head()

# In[ ]:


for app_name, app_id in zip(app_names, app_ids):

    # Get start time
    start = dt.datetime.now(tz=get_localzone())
    fmt= "%m/%d/%y - %T %p"

    # Print starting output for app
    print('---'*20)
    print('---'*20)
    print(f'***** {app_name} started at {start.strftime(fmt)}')
    print()

    # Instantiate AppStore for app
    app_ = AppStore(country='id', app_name=app_name, app_id=app_id)

    # Scrape reviews posted since February 28, 2020 and limit to 10,000 reviews
    app_.review(how_many=10000,
                after=dt.datetime(2020, 2, 28),
                sleep=random.randint(20,25))

    reviews = app_.reviews

    # Add keys to store information about which app each review is for
    for rvw in reviews:
        rvw['app_name'] = app_name
        rvw['app_id'] = app_id

    # Print update that scraping was completed
    print(f"""Done scraping {app_name}.
    Scraped a total of {app_.reviews_count} reviews.\n""")

    # Convert list of dicts to Pandas DataFrame and write to csv
    output_path = '/content/drive/MyDrive/Kuliah/RPL/scraper/AppStore/' + app_name + '.csv'
    #output_path = 'Var/AppStore/' + app_name + '.csv'
    review_df = pd.DataFrame(reviews)
    review_df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

    #save into MongoDB
    comment_collection.insert_many(reviews)

    # Get end time
    end = dt.datetime.now(tz=get_localzone())

    # Print ending output for app
    print(f"""Successfully wrote {app_name} reviews to csv
    at {end.strftime(fmt)}.\n""")
    print(f'Time elapsed for {app_name}: {end-start}')
    print('---'*20)
    print('---'*20)
    print('\n')

    # Wait 5 to 10 seconds to start scraping next app
    time.sleep(random.randint(5,10))
