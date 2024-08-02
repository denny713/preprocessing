import requests
import urllib.parse

from bs4 import BeautifulSoup


def scrape_detik(topik, total_pages):
    hades = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    results = []

    for page in range(1, total_pages):
        query = urllib.parse.quote_plus(topik)
        url = f'https://www.detik.com/search/searchnews?query={query}&sortby=time&page={page}'

        ge = requests.get(url, hades).text
        sop = BeautifulSoup(ge, 'lxml')
        li = sop.find('div', class_='list-content')
        lin = li.find_all('article')

        for x in lin:
            link = x.find('a')['href']
            ge_ = requests.get(link, hades).text
            sop_ = BeautifulSoup(ge_, 'lxml')
            content = sop_.find_all('div', class_='detail__body-text itp_bodycontent')
            for x in content:
                x = x.find_all('p')
                y = [y.text for y in x]
                content_ = (''.join(y).replace('\n', '').replace('ADVERTISEMENT', '')
                            .replace('SCROLL TO RESUME CONTENT', ''))
                print(content_)
                results.append(content_)

    return results
