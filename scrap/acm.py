import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_acm(type, keyword):
    url = 'https://dl.acm.org/action/doSearch?AllField={}'.format(keyword)

    if type == "title":
        return scrape_acm_titles(url)
    elif type == "abstract":
        return scrape_acm_abstracts(url)
    else:
        return []


def scrape_acm_titles(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h5", class_="issue-item__title")

        results = []
        for title in titles:
            results.append(title.text.strip())

        return results
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")
        return []


def scrape_acm_abstracts(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h5", class_="issue-item__title")
        abstracts = soup.find_all("div", class_="issue-item__abstract")
        title_list = [title.text.strip() for title in titles]
        abstract_list = [abstract.text.strip() for abstract in abstracts]
        data = pd.DataFrame({'Judul': title_list, "Abstracts ": abstract_list})
        return data
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")
        return []