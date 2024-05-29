import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_acm_titles():
    url = "https://dl.acm.org/action/doSearch?AllField=machine"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h5", class_="issue-item__title")

        for title in titles:
            print(title.text.strip())
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_acm_titles()
def scrape_acm_abstracts():
    url = "https://dl.acm.org/action/doSearch?AllField=machine"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("h5", class_="issue-item__title")
        abstracts = soup.find_all("div", class_="issue-item__abstract")
        title_list = [title.text.strip() for title in titles]
        abstract_list = [abstract.text.strip() for abstract in abstracts]
        # Create a datatable using pandas
        data = pd.DataFrame({'Judul': title_list, "Abstracts ": abstract_list } )
        print(data)
        
        # Optional: Save the datatable to a CSV file
        data.to_csv("acm_abstracts.csv", index=False)
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_acm_abstracts()