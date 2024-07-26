from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time


def scrape_springer(keyword):
    page_begin = 1
    formated_search = keyword.replace(" ", "+")
    response = requests.get(f"https://link.springer.com/search/page/{page_begin}?query={formated_search}")
    start_soup = BeautifulSoup(response.content, 'lxml')
    total_number_of_pages = int(start_soup.find("span", class_="number-of-pages").text)

    # pages_url = [f"https://link.springer.com/search/page/{n_page}?query={formated_search}" for n_page in
    #              range(page_begin, total_number_of_pages + 1)]

    # Set maximum page
    max_page = 40
    if total_number_of_pages < max_page:
        max_page = total_number_of_pages

    pages_url = [f"https://link.springer.com/search/page/{n_page}?query={formated_search}" for n_page in
                 range(page_begin, max_page + 1)]

    counter = 0
    results = []

    for url in pages_url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        mini_soup = soup.find("ol", class_="content-item-list")

        for article in mini_soup.find_all("li"):
            counter += 1

            try:
                title_link = article.find("a", class_="title")
                full_link = "https://link.springer.com" + title_link["href"]
                res = requests.get(full_link)
                article_soup = BeautifulSoup(res.content, 'lxml')
            except Exception as e:
                continue

            try:

                try:
                    abstract = article_soup.find("div", class_="c-article-section__content").text
                except Exception as e:
                    abstract = np.nan

                results.append(abstract)
                print(abstract)

            except Exception as e:

                try:
                    abstract = article_soup.find("p", class_="Para").text
                except Exception as e:
                    abstract = np.nan

                results.append(abstract)
                print(abstract)

    return results
