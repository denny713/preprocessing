import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def scrape_sciencedirect_data():
    base_url = "https://www.sciencedirect.com/search?qs=machine&pub=EURO%20Journal%20on%20Computational%20Optimization&cid=778416"
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

    # Save data to CSV
    with open('sciencedirect_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['No', 'Title', 'Full Abstract', 'Cited By', 'Authors', 'Link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print("Data saved to sciencedirect_data.csv")

if __name__ == "__main__":
    scrape_sciencedirect_data()