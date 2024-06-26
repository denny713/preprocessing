#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install google-api-python-client

# In[2]:


import googleapiclient.discovery
from datetime import datetime
from tabulate import tabulate
import json

# Masukkan kunci API Anda di sini
api_key = 'AIzaSyB1Vil81Cp4pFYU6IynwYqynBo9t1CCn2c'

# Fungsi untuk mendapatkan semua komentar beserta total "like" dan datetime berdasarkan ID video
def get_all_video_comments(video_id):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Lakukan request pertama untuk mendapatkan komentar
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=1000  # Ubah sesuai kebutuhan
    ).execute()

    # Ambil komentar beserta total "like" dan datetime dari respons
    comments_data = []
    for item in response['items']:
        comment_data = {
            'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
            'like_count': item['snippet']['topLevelComment']['snippet']['likeCount'],
            'datetime': item['snippet']['topLevelComment']['snippet']['publishedAt']
        }
        comments_data.append(comment_data)

    # Periksa apakah masih ada halaman berikutnya
    while 'nextPageToken' in response:
        nextPageToken = response['nextPageToken']
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=1000,  # Ubah sesuai kebutuhan
            pageToken=nextPageToken
        ).execute()

        # Ambil komentar dari halaman berikutnya
        for item in response['items']:
            comment_data = {
                'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                'like_count': item['snippet']['topLevelComment']['snippet']['likeCount'],
                'datetime': item['snippet']['topLevelComment']['snippet']['publishedAt']
            }
            comments_data.append(comment_data)

    return comments_data

# Contoh penggunaan
video_id = 'BmPyB4rzV2I'
all_comments_data = get_all_video_comments(video_id)

# Mengurutkan komentar berdasarkan tanggal terbaru
sorted_comments_data = sorted(all_comments_data, key=lambda x: datetime.strptime(x['datetime'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

# Tampilkan komentar beserta total "like" dan datetime
for index, comment_data in enumerate(all_comments_data, start=1):
    comment_datetime = datetime.strptime(comment_data['datetime'], '%Y-%m-%dT%H:%M:%SZ')
    formatted_datetime = comment_datetime.strftime('%Y-%m-%d %H:%M:%S')

    print(f'Comment {index}: {comment_data["text"]}')
    print(f'Total Like: {comment_data["like_count"]}')
    print(f'Datetime: {formatted_datetime}\n')

# In[3]:


check_out = []
check_out.append(sorted_comments_data)

# In[4]:


# Menyimpan data ke file JSON di direktori
json_file_path = r'C:\Users\tsaqi\Documents\Scraper\Fardan\Tugas Scrapper KCI Sosmed\comments_data_sorted.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_comments_data, json_file, indent=2)

print(f'Data berhasil disimpan dalam file JSON: {json_file_path}')

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

# In[ ]:


client.stats

# In[ ]:


youtube_comments_db = client['youtube_comments_db']
comments_collection = youtube_comments_db['comments_collection']
comments_collection.insert_many(sorted_comments_data)
