#!/usr/bin/env python
# coding: utf-8

# In[1]:


!pip install timed_count
!pip install pymongo[srv]

# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
from threading import Thread
from timed_count import timed_count

from pprint import pprint

import datetime as dt
from tzlocal import get_localzone

import random
import time
import os

# In[3]:


# from google.colab import drive
# drive.mount('/content/drive')

# In[4]:


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


StackOverflow_db = client['StackOverflow_db']

info_collection = StackOverflow_db['info_collection']

comment_collection = StackOverflow_db['comment_collection']

# In[ ]:


target = 'StackOverflow'

# In[ ]:


def scrap(data):
    allData = []
    start = dt.datetime.now(tz=get_localzone())
    fmt = "%m/%d/%y - %T %p"
    # Print starting output for app
    print('---'*20)
    print('---'*20)
    print(f'***** {target} started at {start.strftime(fmt)}')
    print()
    # looping data to scrap more details
    for item in data:
        # define target scrap based on question id
        url = 'https://stackoverflow.com/questions/' + str(item['question_id'])
        # make request to api
        req = requests.get(url)
        # parsing request with Beautifulsoup html parser
        soup = BeautifulSoup(req.text, 'html.parser')
        # defining variables
        question_id = str(item['question_id'])
        title = soup.find('a', {'class': 'question-hyperlink'}).text.strip() # type: ignore
        content = soup.find('div', {'class': 'js-post-body'}).text.strip()  # type: ignore
        post_tag = str(item['tags'])[1:-1]
        if str(item['owner']['user_id']) != '':
          user_id = str(item['owner']['user_id'])
        else:
          user_id = '-'
        question_stamp = soup.time.attrs # type: ignore
        # Array untuk menyimpan hasil scraping
        answers_data = []

        # Find all answer divs
        answer_divs = soup.find_all('div', {'class': 'answer'})

        # Extract information from each answer
        for i, answer_div in enumerate(answer_divs):
            if i < 3:  # Adjust the number to the desired number of answers to display
                # Extract user_id
                user_id_tag = answer_div.find('div', {'itemprop': 'author'}).find('a')
                answer_user_id = user_id_tag['href'].split('/')[-2] if user_id_tag else "Kosong"
                # Extract answer text
                answer_text_tag = answer_div.find('div', {'class': 's-prose'})
                answer_text = answer_text_tag.text.strip() if answer_text_tag else "Kosong"

                # Extract upvote count
                upvote_count_tag = answer_div.find('div', {'class': 'js-vote-count'})
                upvote_count = upvote_count_tag.text.strip() if upvote_count_tag else "0"

                # Extract answer time based on user-action-time
                answer_time_tag = answer_div.find('div', {'class': 'user-action-time'}).find('span', {'class': 'relativetime'})
                answer_time = answer_time_tag['title'].replace('Z', '') if answer_time_tag else "Kosong"

                # Extract comments for each answer
                comments = []
                comments_list = answer_div.find('ul', {'class': 'comments-list'})
                if comments_list:
                    for comment_div in comments_list.find_all('li', {'class': 'comment'}):
                        # Extract comment text
                        comment_text_tag = comment_div.find('span', {'class': 'comment-copy'})
                        comment_text = comment_text_tag.text.strip() if comment_text_tag else "Kosong"

                        # Extract comment user_id
                        comment_user_id_tag = comment_div.find('a', {'class': 'comment-user'})
                        comment_user_id = comment_user_id_tag['href'].split('/')[-2] if comment_user_id_tag else "Kosong"

                        # Extract comment date
                        comment_date_tag = comment_div.find('span', {'class': 'relativetime-clean'})
                        comment_date = comment_date_tag['title'].replace('Z, License: CC BY-SA ', '').replace('3.0', '').replace('4.0', '').replace('5.0', '') if comment_date_tag else "Kosong"

                        comments.append({'comment_text': comment_text, 'comment_user_id': comment_user_id, 'comment_date': comment_date})

                # Menyimpan data jawaban ke dalam array
                answer_data = {
                    'answer_user_id': answer_user_id,
                    'answer_text': answer_text,
                    'answer_time': answer_time,
                    'upvote_count': upvote_count,
                    'comments': comments
                }
                answers_data.append(answer_data)
        # appending item to array
        allData.append({'question_id': question_id,'title': title, 'content': content, 'post_tag': post_tag, 'user_id': user_id, 'question_stamp': question_stamp['datetime'], 'answers': answers_data})
        time.sleep(1.0)
    #Save into MongoDB
    comment_collection.insert_many(allData)
    # transform array to Pandas DataFrame
    check_out = pd.DataFrame(allData)
    # output path for storing data
    output_path = '/content/drive/MyDrive/Kuliah/RPL/scraper/' + target + '.csv'
    # storing data into csv format
    check_out.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
    allData.clear()
    end = dt.datetime.now(tz=get_localzone())
    print(f"""
        Successfully inserted {len(check_out)} {target} Questions into collection
        at {end.strftime(fmt)}.\n
        """)
    print(f'Time elapsed for {target}: {end-start}')
    print('---'*20)
    print('---'*20)
    print('\n')

# In[ ]:


question_count = 10
for count in timed_count(120):
    api = requests.get(
        'https://api.stackexchange.com/2.3/search/advanced?pagesize='+
        str(question_count) +'&order=desc&sort=activity&site=stackoverflow').json()
    data = api['items']
    scrap(data)

# In[ ]:


api = requests.get(
        'https://api.stackexchange.com/2.3/search/advanced?pagesize=2&order=desc&sort=activity&site=stackoverflow').json()
data = api['items']
scrap(data)
