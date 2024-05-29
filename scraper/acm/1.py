import requests
from bs4 import BeautifulSoup

def scrape_acm_abstracts():
    url = "https://dl.acm.org/action/doSearch?AllField=machine"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        abstracts = soup.find_all("div", class_="issue-item__abstract")

        for abstract in abstracts:
            print(abstract.text.strip())
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_acm_abstracts()
