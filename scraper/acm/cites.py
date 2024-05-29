import requests
from bs4 import BeautifulSoup

def scrape_acm_authors():
    url = "https://dl.acm.org/action/doSearch?AllField=machine"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        authors_elements = soup.find_all("span", class_="hlFld-ContribAuthor")

        authors_list = []
        for authors_element in authors_elements:
            author_name = authors_element.text.strip()
            authors_list.append(author_name)

        print("Authors:")
        for author in authors_list:
            print(author)
    else:
        print(f"Error: Unable to fetch the content. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_acm_authors()