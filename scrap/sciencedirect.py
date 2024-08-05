import urllib.parse

import requests
from bs4 import BeautifulSoup


def scrap_sciencedirect(keyword, pub, cid):
    keyword = urllib.parse.quote(keyword)
    pub = urllib.parse.quote(pub)
    base_url = f"https://www.sciencedirect.com/search?qs={keyword}&pub={pub}&cid={cid}"
    data = []
    page_num = 1

    while True:
        url = f"{base_url}&offset={page_num * 10 - 10}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("div", class_="result-item")

            if not articles:
                break

            for index, article in enumerate(articles, start=1):
                title = article.find("h2", class_="result-item-title").text.strip()
                abstract_element = article.find("div", class_="abstract author")
                abstract = abstract_element.text.strip() if abstract_element else ""
                cited_by = article.find("div", class_="text-xs").text.strip().split("Cited by ")[-1]
                authors = [author.text.strip() for author in article.find_all("a", class_="author")]
                link = article.find("a", class_="result-item-link")['href']

                data.append({
                    'No': len(data) + 1,
                    'Title': title,
                    'Full Abstract': abstract,
                    'Cited By': cited_by,
                    'Authors': ', '.join(authors),
                    'Link': link
                })

            page_num += 1

        else:
            print(f"Error: Unable to fetch the content for page {page_num}. Status code: {response.status_code}")
            break

    print(data)
    return data
