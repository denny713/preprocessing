#!/usr/bin/env python
# coding: utf-8

# In[1]:


!pip install pymongo[srv]
!pip install google-play-scraper

# In[2]:


import pandas as pd

from google_play_scraper import app, Sort, reviews

from pprint import pprint

import pymongo
from pymongo import MongoClient

import datetime as dt
from tzlocal import get_localzone

import random
import time

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


Play_store_db = client['Play_store_db']

info_collection = Play_store_db['info_collection']

comment_collection = Play_store_db['comment_collection']

# In[ ]:


client.stats                                # .stats  show details about the client

# In[ ]:


# app_df = pd.read_csv('Var/PlayStore/ScrapApp.csv.csv')
# app_df.head()
app_name = []
android_appID = []

# In[ ]:


['SpongeBob Adventures In A Jam', 'SpongeBob Cooking Fever']
['com.tiltingpoint.sbadventures', 'com.tiltingpoint.spongebob']

# In[ ]:


# number of apps as input
n = int(input("Enter number of apps : "))

# iterating till the range
for i in range(0, n):
    appName = input("Enter App Name: ")
    appID = input("Enter App ID: ")
    # adding the appName and appID
    app_name.append(appName)
    android_appID.append(appID)

print(app_name)
print(android_appID)

# In[ ]:


app_names = list(app_name)
app_ids = list(android_appID)

# In[ ]:


app_info = []
for i in app_ids:
    info = app(i)
    del info['comments']
    app_info.append(info)

pprint(app_info[0])

# In[ ]:


info_collection.insert_many(app_info)

# In[ ]:


info_df = pd.DataFrame(list(info_collection.find({})))
info_df.head()

# In[ ]:


for app_name, app_id in zip(app_names, app_ids):

    start = dt.datetime.now(tz=get_localzone())
    fmt= "%m/%d/%y - %T %p"

    print('---'*20)
    print('---'*20)
    print(f'***** {app_name} started at {start.strftime(fmt)}')
    print()

    app_reviews = []

    count = 200

    batch_num = 0

    # Retrieve reviews (and continuation_token) with reviews function
    rvws, token = reviews(
        app_id,           # found in app's url
        lang='en',        # defaults to 'en'
        country='us',     # defaults to 'us'
        sort=Sort.NEWEST, # start with most recent
        count=count       # batch size
    )  # type: ignore

    for r in rvws:
        r['app_name'] = app_name # add key for app's name
        r['app_id'] = app_id     # add key for app's id


    app_reviews.extend(rvws)

    batch_num +=1
    print(f'Batch {batch_num} completed.')

    time.sleep(random.randint(1,5))

    pre_review_ids = []
    for rvw in app_reviews:
        pre_review_ids.append(rvw['reviewId'])

    for batch in range(4999):
        rvws, token = reviews( # store continuation_token
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count,
            # using token obtained from previous batch
            continuation_token=token
        )

        new_review_ids = []
        for r in rvws:
            new_review_ids.append(r['reviewId'])

            r['app_name'] = app_name # add key for app's name
            r['app_id'] = app_id     # add key for app's id

        app_reviews.extend(rvws)

        batch_num +=1

        # Break loop and stop scraping for current app if most recent batch
        # did not add any unique reviews
        all_review_ids = pre_review_ids + new_review_ids
        if len(set(pre_review_ids)) == len(set(all_review_ids)):
            print(f'No reviews left to scrape. Completed {batch_num} batches.\n')
            break

        # all_review_ids becomes pre_review_ids to check against
        # for next batch
        pre_review_ids = all_review_ids

        # At every 100th batch
        if batch_num%100==0:

            # print update on number of batches
            print(f'Batch {batch_num} completed.')

            # insert reviews into collection
            comment_collection.insert_many(app_reviews) #MongoDB

            output_path = '/content/drive/MyDrive/Kuliah/RPL/scraper/PlayStore/results/' + app_name + '.csv'
            review_df = pd.DataFrame(app_reviews)
            review_df.to_csv(output_path, mode='a', header=not os.path.exists(output_path)) #CSV

            # print update about num reviews inserted
            store_time = dt.datetime.now(tz=get_localzone())
            print(f"""
            Successfully inserted {len(app_reviews)} {app_name}
            reviews into collection at {store_time.strftime(fmt)}.\n
            """)

            # empty our list for next round of 100 batches
            app_reviews = []

        time.sleep(random.randint(1,5))

    # Print update when max number of batches has been reached
    # OR when last batch didn't add any unique reviews
    print(f'Done scraping {app_name}.')
    print(f'Scraped a total of {len(set(pre_review_ids))} unique reviews.\n')


    # Insert remaining reviews into collection
    comment_collection.insert_many(app_reviews)

    output_path = '/content/drive/MyDrive/Kuliah/RPL/scraper/PlayStore/results/' + app_name + '.csv'
    review_df = pd.DataFrame(app_reviews)
    review_df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

    # Get end time
    end = dt.datetime.now(tz=get_localzone())

    # Print ending output for app
    print(f"""
    Successfully inserted all {app_name} reviews into collection
    at {end.strftime(fmt)}.\n
    """)
    print(f'Time elapsed for {app_name}: {end-start}')
    print('---'*20)
    print('---'*20)
    print('\n')

    time.sleep(random.randint(1,5))
