#!/usr/bin/env python
# coding: utf-8

# In[1]:


#library yang digunakan
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# In[3]:


#input pencarian dengan 2 kata
key = input("Cari kata:")
key1 = input("Cari: ")
hal = input("jumlah halaman 10,20,50:")
#scrape file data
def scrape_acm_data():
    base_url = "https://dl.acm.org/action/doSearch?AllField={}+{}&expand=dl&startPage=".format(key,key1)
    data = []

    page_num = 1

    while True:
        url = f"{base_url}{page_num}&pageSize=".format(hal)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("div", class_="issue-item")

            if not articles:
                break

            for index, article in enumerate(articles, start=1):
                title = article.find("h5", class_="issue-item__title").text.strip()
                abstract = article.find("div", class_="issue-item__abstract").text.strip()
                #cited_by = article.find("div", class_="issue-item__meta--cited-by").text.strip().split("Cited by ")[-1]
                authors = [author.text.strip() for author in article.find_all("span", class_="hlFld-ContribAuthor")]
                #link_download = article.find("a", class_="issue-item__title").get('href')
                doi = article.find("a", class_="issue-item__doi").text.strip()

                data.append({
                    'No': len(data) + 1,
                    'Title': title,
                    'Abstract': abstract,
                    #'Cited By': cited_by,
                    'Authors': authors,
                    'Doi': doi
                    #'Link Download': link_download
                })

            page_num += 1

        else:
            print(f"Error: Gagal page {page_num}. Status code: {response.status_code}")
            break

    # Simpan data to CSV 'Cited By',, 'Link Download'
    with open('{}_acm_data_{}{}.csv'.format(hal, key, key1), mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['No', 'Title', 'Abstract', 'Authors' , 'Doi']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print("Data saved to {}_acm_data_{}{}.csv".format(hal, key, key1))

if __name__ == "__main__":
    scrape_acm_data()


# In[ ]:


#menampilkan data scv hasil scrapper
df = pd.read_csv('{}_acm_data_{}{}.csv'.format(hal, key, key1))
df
