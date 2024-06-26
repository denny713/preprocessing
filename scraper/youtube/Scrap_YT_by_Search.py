#!/usr/bin/env python
# coding: utf-8

# In[1]:


from googleapiclient.discovery import build
from datetime import datetime

# Ganti 'YOUR_API_KEY' dengan kunci API yang Anda dapatkan dari Google Developer Console
api_key = 'AIzaSyB1Vil81Cp4pFYU6IynwYqynBo9t1CCn2c'
youtube = build('youtube', 'v3', developerKey=api_key)

# Ambil ID video, komentar, dan tanggal dari video
def get_video_data(query, max_results=5):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    video_data_list = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            comments = get_video_comments(video_id)
            video_data = {'video_id': video_id, 'comments': comments}
            video_data_list.append(video_data)

    return video_data_list

# Ambil komentar, tanggal, dan waktu dari video
def get_video_comments(video_id):
    comments_data = []

    comment_threads = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Ubah sesuai kebutuhan Anda
    ).execute()

    for comment_thread in comment_threads['items']:
        comment_snippet = comment_thread['snippet']['topLevelComment']['snippet']
        comment_text = comment_snippet['textDisplay']
        comment_datetime = comment_snippet['publishedAt']
        comment_datetime = datetime.strptime(comment_datetime, '%Y-%m-%dT%H:%M:%SZ')
        
        comments_data.append({'text': comment_text, 'datetime': comment_datetime})

    return comments_data

# Gunakan fungsi-fungsi di atas
search_query = '#jokowi'  # Ganti dengan kata kunci pencarian yang diinginkan
max_results = 3  # Ganti sesuai kebutuhan Anda

video_data_list = get_video_data(search_query, max_results)

# Susun hasil dalam bentuk tabel
print(f"{'Video ID': <20}{'Comment': <60}{'Datetime'}")
print("="*200)

for video_data in video_data_list:
    video_id = video_data['video_id']
    comments = video_data['comments']
    
    for comment_data in comments:
        comment_text = comment_data['text']
        comment_datetime = comment_data['datetime']
        print(f"{video_id: <20}{comment_text: <60}{comment_datetime}")

    print("\n")


# In[2]:


import json
from googleapiclient.discovery import build
from datetime import datetime

# Ganti 'YOUR_API_KEY' dengan kunci API yang Anda dapatkan dari Google Developer Console
api_key = 'AIzaSyB1Vil81Cp4pFYU6IynwYqynBo9t1CCn2c'
youtube = build('youtube', 'v3', developerKey=api_key)

# Ambil ID video, komentar, dan tanggal dari video
def get_video_data(query, max_results=5):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    video_data_list = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            comments = get_video_comments(video_id)
            video_data = {'video_id': video_id, 'comments': comments}
            video_data_list.append(video_data)

    return video_data_list

# Ambil komentar, tanggal, dan waktu dari video
def get_video_comments(video_id):
    comments_data = []

    comment_threads = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Ubah sesuai kebutuhan Anda
    ).execute()

    for comment_thread in comment_threads['items']:
        comment_snippet = comment_thread['snippet']['topLevelComment']['snippet']
        comment_text = comment_snippet['textDisplay']
        comment_datetime = comment_snippet['publishedAt']
        comment_datetime = datetime.strptime(comment_datetime, '%Y-%m-%dT%H:%M:%SZ')
        
        comments_data.append({'text': comment_text, 'datetime': comment_datetime})

    return comments_data

# Gunakan fungsi-fungsi di atas
search_query = 'Python programming tutorial'  # Ganti dengan kata kunci pencarian yang diinginkan
max_results = 3  # Ganti sesuai kebutuhan Anda

video_data_list = get_video_data(search_query, max_results)

# Susun hasil dalam bentuk dictionary
data = {'videos': []}

for video_data in video_data_list:
    video_id = video_data['video_id']
    comments = video_data['comments']
    
    video_entry = {'video_id': video_id, 'comments': []}
    
    for comment_data in comments:
        comment_text = comment_data['text']
        comment_datetime = comment_data['datetime'].isoformat()
        comment_entry = {'text': comment_text, 'datetime': comment_datetime}
        
        video_entry['comments'].append(comment_entry)

    data['videos'].append(video_entry)

# Simpan data dalam format JSON di direktori yang diinginkan
output_path = r'C:\Users\tsaqi\Documents\Scraper\Fardan\Tugas Scrapper KCI Sosmed\youtube_data.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)


# In[ ]:



