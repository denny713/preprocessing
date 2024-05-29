import requests
from bs4 import BeautifulSoup
import sqlite3

##key = input('nama jurnal:')
def scrape_acm_data():
    url = "https://dl.acm.org/action/doSearch?AllField=".format('machine')
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h5", class_="issue-item__title")
        abstracts = soup.find_all("div", class_="issue-item__abstract")

        # Connect to SQLite database
        conn = sqlite3.connect('acm_data.db')
        cursor = conn.cursor()

        # Iterate through titles and abstracts
        for title, abstract in zip(titles, abstracts):
            title_text = title.text.strip()
            abstract_text = abstract.text.strip()

            # Insert data into database
            cursor.execute("INSERT INTO acm_data (title, abstract) VALUES (?, ?)", (title_text, abstract_text))

        # Commit changes and close connection
        conn.commit()
        conn.close()
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_acm_data()