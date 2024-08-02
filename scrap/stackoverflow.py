import requests
from bs4 import BeautifulSoup


def scrape_stack_overflow(page_size):
    api = requests.get(
        'https://api.stackexchange.com/2.3/search/advanced?pagesize=' +
        str(page_size) + '&order=desc&sort=activity&site=stackoverflow').json()
    data = api['items']

    return scrap(data)


def scrap(data):
    allData = []
    for item in data:
        url = 'https://stackoverflow.com/questions/' + str(item['question_id'])
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        question_id = str(item['question_id'])
        title = soup.find('a', {'class': 'question-hyperlink'}).text.strip()  # type: ignore
        content = soup.find('div', {'class': 'js-post-body'}).text.strip()  # type: ignore
        post_tag = str(item['tags'])[1:-1]
        if str(item['owner']['user_id']) != '':
            user_id = str(item['owner']['user_id'])
        else:
            user_id = '-'
        question_stamp = soup.time.attrs  # type: ignore
        answers_data = []
        answer_divs = soup.find_all('div', {'class': 'answer'})

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
                answer_time_tag = answer_div.find('div', {'class': 'user-action-time'}).find('span',
                                                                                             {'class': 'relativetime'})
                answer_time = answer_time_tag['title'].replace('Z', '') if answer_time_tag else "Kosong"

                # Extract comments for each answer
                comments = []
                comments_list = answer_div.find('ul', {'class': 'comments-list'})
                if comments_list:
                    for comment_div in comments_list.find_all('li', {'class': 'comment'}):
                        comment_text_tag = comment_div.find('span', {'class': 'comment-copy'})
                        comment_text = comment_text_tag.text.strip() if comment_text_tag else "Kosong"

                        comment_user_id_tag = comment_div.find('a', {'class': 'comment-user'})
                        comment_user_id = comment_user_id_tag['href'].split('/')[
                            -2] if comment_user_id_tag else "Kosong"

                        comment_date_tag = comment_div.find('span', {'class': 'relativetime-clean'})
                        comment_date = (comment_date_tag['title'].replace('Z, License: CC BY-SA ', '')
                                        .replace('3.0', '').replace('4.0', '')
                                        .replace('5.0', '')) if comment_date_tag else "Kosong"

                        comments.append({'comment_text': comment_text,
                                         'comment_user_id': comment_user_id,
                                         'comment_date': comment_date})

                answer_data = {
                    'answer_user_id': answer_user_id,
                    'answer_text': answer_text,
                    'answer_time': answer_time,
                    'upvote_count': upvote_count,
                    'comments': comments
                }
                answers_data.append(answer_data)

        allData.append(
            {'question_id': question_id, 'title': title, 'content': content, 'post_tag': post_tag, 'user_id': user_id,
             'question_stamp': question_stamp['datetime'], 'answers': answers_data})

    print("All data: ", allData)
    return allData
