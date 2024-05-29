import requests
from bs4 import BeautifulSoup
import csv

def scrape_acm_data():
    url = "https://dl.acm.org/action/doSearch?AllField=machine"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="issue-item")

        # Create a CSV file
        with open('acm_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['cites', 'peryear', 'Rank', 'Authors', 'year', 'publication', 'publisher', 'type', 'abstract']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            # Iterate through articles
            for article in articles:
                cites = int(article.find("div", class_="citation").text.strip())
                peryear = int(article.find("div", class_="issue-item__per-year").text.strip())
                rank = int(article.find("div", class_="issue-item__rank").text.strip())
                authors = article.find("div", class_="issue-item__authors").text.strip()
                year = int(article.find("div", class_="issue-item__year").text.strip())
                publication = article.find("div", class_="issue-item__publication").text.strip()
                publisher = article.find("div", class_="issue-item__publisher").text.strip()
                type = article.find("div", class_="issue-item__type").text.strip()
                abstract = article.find("div", class_="issue-item__abstract").text.strip()

                # Write data to CSV
                writer.writerow({
                    'cites': cites,
                    'peryear': peryear,
                    'Rank': rank,
                    'Authors': authors,
                    'year': year,
                    'publication': publication,
                    'publisher': publisher,
                    'type': type,
                    'abstract': abstract
                })

        print("Data written to acm_data.csv")
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_acm_data()
