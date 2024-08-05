from googleapiclient.discovery import build
from datetime import datetime


def scrap_youtube(keyword, max_result):
    api_key = 'AIzaSyB1Vil81Cp4pFYU6IynwYqynBo9t1CCn2c'
    youtube = build('youtube', 'v3', developerKey=api_key)

    results = get_video_data(youtube, keyword, max_result)
    print(results)

    return results


def get_video_data(youtube, query, max_results):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    video_data_list = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            comments = get_video_comments(youtube, video_id)
            video_data = {'video_id': video_id, 'comments': comments}
            video_data_list.append(video_data)

    return video_data_list


def get_video_comments(youtube, video_id):
    comments_data = []

    comment_threads = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    ).execute()

    for comment_thread in comment_threads['items']:
        comment_snippet = comment_thread['snippet']['topLevelComment']['snippet']
        comment_text = comment_snippet['textDisplay']
        comment_datetime = comment_snippet['publishedAt']
        comment_datetime = datetime.strptime(comment_datetime, '%Y-%m-%dT%H:%M:%SZ')

        comments_data.append({'text': comment_text, 'datetime': comment_datetime})

    return comments_data
