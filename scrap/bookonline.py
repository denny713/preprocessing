import numpy as np
import requests

from bs4 import BeautifulSoup
from urllib.parse import quote


def scrape_bookonline(judul):
    judul = quote(judul)
    uri = 'https://www.goodreads.com/search?utf8=%E2%9C%93&search_type=books&q=' + judul
    print(uri)

    count = 0
    results = []

    response = requests.get(uri)
    soup = BeautifulSoup(response.content, 'lxml')
    mini_soup = soup.find("table", class_="tableList")
    print(soup)

    for article in mini_soup.find_all("tr"):
        count += 1

        try:
            title_link = article.find("a", class_="bookTitle")
            full_link = "https://www.goodreads.com/" + title_link["href"]
            print(full_link)
            res = requests.get(full_link)
            article_soup = BeautifulSoup(res.content, 'lxml')
        except Exception as e:
            continue

        try:
            abstract = article_soup.find("div", class_="DetailsLayoutRightParagraph__widthConstrained").text
        except Exception as e:
            abstract = np.nan

        results.append(abstract)
        print(abstract)

    return results
