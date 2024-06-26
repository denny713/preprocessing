#!/usr/bin/env python
# coding: utf-8

# In[7]:


#AUTHORID = 'YA8f5tQAAAAJ'
AUTHORID = 'aegDFT4AAAAJ'

DATA_PATH = ''
# from google.colab import drive
# #drive.mount('/content/drive')
# drive.mount('/content/drive')
# #DATA_PATH = '/content/drive/MyDrive/RPL'
# DATA_PATH = '/content/drive'

# In[8]:


!pip install beautifulsoup4
import json, requests, bs4, re, time, sys
import openpyxl
from bs4 import BeautifulSoup
import csv
import pandas as pd

# In[13]:


class Publication(object):
  def __init__(self, title, year, cited_by,
               link=None,
               authors=None,
               description=None,
               citation_histogram=None,
               detail_extracted=False,
               url=None,
               cookies=None):

    self.cookies = cookies
    self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    self.url = url
    self.soup = None

    self.title = title
    self.year = year
    self.cited_by = cited_by
    self.link = link
    self.authors = authors
    self.description = description
    self.citation_histogram = citation_histogram
    self.detail_extracted = detail_extracted

  def set_url(self):
    return f'https://scholar.google.com/citations?{self.url}'

  def make_detail_request(self):
    url = self.set_url()
    response = requests.request("GET",url,headers=self.headers,cookies=self.cookies)
    if response.status_code == 200:
      self.detail_extracted = True
    return response

  # TODO: For some reason, stopped working.
  # The response html is different and does not contain this information)
  def get_link_to_publication(self):
    title = self.soup.find('div', {'id': 'gsc_oci_title'})
    if title:
      link = title.find('a', {'class': 'gsc_oci_title_link'})
      if link:
        self.link = link.get('href')

  def get_authors(self):
    authors = self.soup.find('div', text = re.compile('Authors'), attrs = {'class' : 'gsc_oci_field'})
    if authors:
      self.authors = authors.parent.find('div', {'class': 'gsc_oci_value'}).get_text().split(', ')
    else:
      inventors = self.soup.find('div', text = re.compile('Inventors'), attrs = {'class' : 'gsc_oci_field'})
      if inventors:
        self.authors = inventors.parent.find('div', {'class': 'gsc_oci_value'}).get_text().split(', ')

  # TODO: For some reason, stopped working.
  # The response html is different and does not contain this information)
  def get_description(self):
    description = self.soup.find('div', {'id': 'gsc_oci_descr'})
    if description:
      self.description = description.get_text()

  def get_citation_histogram(self):
    citation_hist = self.soup.find('div', {'id': 'gsc_oci_graph_bars'})
    if citation_hist:
      citation_hist_time = list(map(lambda x: int(x.get_text()),citation_hist.find_all('span', {'class': 'gsc_oci_g_t'})))
      citation_hist_cites = list(map(lambda x: int(x.get_text()),citation_hist.find_all('span', {'class': 'gsc_oci_g_al'})))
      self.citation_histogram = list(zip(citation_hist_time,citation_hist_cites))

  def scrape(self):
    self.soup = bs4.BeautifulSoup(self.make_detail_request().content, 'lxml')
    if self.detail_extracted:
      self.get_link_to_publication()
      self.get_authors()
      self.get_description()
      self.get_citation_histogram()
    return self.detail_extracted

  def export_json(self):
    return {'url': self.url,
            'title': self.title,
            'link': self.link,
            'year': self.year,
            'cited_by': self.cited_by,
            'authors': self.authors,
            'description': self.description,
            'citation_histogram': self.citation_histogram,
            'detail_extracted': self.detail_extracted}


class Author(object):
  data_path = DATA_PATH

  def __init__(self, authorID,
               name=None,
               image_link=None,
               interests=None,
               citations=None,
               hindex=None,
               i10index=None,
               citation_histogram=None,
               coauthors=None,
               publications=None,
               all_publications_retrieved=False,
               all_publications_extracted=False,
               cstart=0,
               pagesize=100, # Max page size in scholar
               cookies=None):

    self.cstart = cstart
    self.pagesize = pagesize
    self.cookies = cookies
    self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    self.soup = None

    self.authorID = authorID
    self.name = name
    self.image_link = image_link
    self.interests = interests
    self.citations = citations
    self.hindex = hindex
    self.i10index = i10index
    self.citation_histogram = citation_histogram
    self.coauthors = coauthors
    self.publications = publications
    self.all_publications_retrieved = all_publications_retrieved
    self.all_publications_extracted = all_publications_extracted

  def set_url(self):
    return f"https://scholar.google.com/citations?hl=en&user={self.authorID}&cstart={self.cstart}&pagesize={self.pagesize}"

  def make_profile_request(self):
    url = self.set_url()
    response = requests.request("GET",url,headers=self.headers,cookies=self.cookies)
    if response.status_code == 429:
      raise Exception("The server responded with Error 429. We have been detected. Wait before trying again.")
    self.cookies = response.cookies
    return response

  def get_soup(self):
    self.soup = bs4.BeautifulSoup(self.make_profile_request().content, 'html.parser')

  def make_coauthor_request(self):
    url = self.set_url()+'&view_op=list_colleagues'
    response = requests.request("GET",url,headers=self.headers)
    if response.status_code == 429:
      raise Exception("The server responded with Error 429. We have been detected. Wait before trying again.")
    return response

  def get_full_name(self):
    name = self.soup.find('div', {'id': 'gsc_prf_in'})
    if name:
      self.name = name.get_text()

  # TODO: For some reason, stopped working.
  # The response html is different and does not contain this information)
  def get_image_link(self):
    image = self.soup.find('div', {'img': 'gsc_prf_pup-img'})
    if image:
      self.image_link = image.get('src')

  def get_interests(self):
    self.interests = list(map(lambda x: x.get_text(), self.soup.find_all('a', {'class': 'gsc_prf_inta'})))

  def get_citations_count(self, citation_info):
    citation = citation_info.find('a', text = re.compile('Citations'), attrs = {'class' : 'gsc_rsb_f'})
    if citation:
      citation_value = citation.parent.parent.find_all('td', {'class': 'gsc_rsb_std'})
      if len(citation_value)>0:
        self.citations = int(citation_value[0].get_text())

  def get_hindex(self, citation_info):
    hindex = citation_info.find('a', text = re.compile('h-index'), attrs = {'class' : 'gsc_rsb_f'})
    if hindex:
      hindex_value = hindex.parent.parent.find_all('td', {'class': 'gsc_rsb_std'})
      if len(hindex_value)>0:
        self.hindex = int(hindex_value[0].get_text())

  def get_i10index(self, citation_info):
    i10index = citation_info.find('a', text = re.compile('i10-index'), attrs = {'class' : 'gsc_rsb_f'})
    if i10index:
      i10index_value = i10index.parent.parent.find_all('td', {'class': 'gsc_rsb_std'})
      if len(i10index_value)>0:
        self.i10index = int(i10index_value[0].get_text())

  def get_citation_metrics(self):
    citation_info = self.soup.find('div', {'id': 'gsc_rsb_cit'})
    if citation_info:
      self.get_citations_count(citation_info)
      self.get_hindex(citation_info)
      self.get_i10index(citation_info)

  def get_citation_histogram(self):
    citation_hist = self.soup.find_all('div', {'class': 'gsc_md_hist_w'})
    if citation_hist:
      citation_hist = citation_hist[0]
      citation_hist_time = list(map(lambda x: x.get_text(),citation_hist.find_all('span', {'class': 'gsc_g_t'})))
      citation_hist_cites = list(map(lambda x: x.get_text(),citation_hist.find_all('a', {'class': 'gsc_g_a'})))
      self.citation_histogram = list(zip(citation_hist_time,citation_hist_cites))

  def get_coauthors(self):
    coauthor_list = self.soup.find('div', {'id': 'gsc_rsb_co'})
    if coauthor_list:
      if coauthor_list.find('button'): # too many coauthors requires a request
        coauthor_list = bs4.BeautifulSoup(self.make_coauthor_request().content, 'html.parser').find('div', {'id': 'gsc_codb_content'})
        coauthor_list = coauthor_list.find_all('div', {'class': 'gsc_ucoar'})
        coauthor_ids = list(map(lambda x: x.get('id').split('-')[-1], coauthor_list))
        coauthor_names = list(map(lambda x: x.find('img').get('alt'), coauthor_list))
        self.coauthors = list(zip(coauthor_ids,coauthor_names))
      else:
        coauthor_list = coauthor_list.find_all('img')
        coauthor_ids = list(map(lambda x: x.get('id').split('-')[1], coauthor_list))
        coauthor_names = list(map(lambda x: x.get('alt'), coauthor_list))
        self.coauthors = list(zip(coauthor_ids,coauthor_names))

  def extract_compact_publication(self, publication_element):
    title = publication_element.find('a',{"class": "gsc_a_at"}).get_text()
    year = publication_element.find('td',{"class": "gsc_a_y"}).find('span', {"class": "gsc_a_hc"}).get_text()
    if year:
      year = int(year)
    else:
      year = None
    url = publication_element.find('a',{"class": "gsc_a_at"}).get('href').split('?')[-1]
    cited_by = publication_element.find('a',{"class": "gsc_a_ac"}).get_text()
    if cited_by:
      cited_by = int(cited_by)
    else:
      cited_by = None
    return Publication(title, year, cited_by, url=url, cookies=self.cookies)

  def get_publications_list(self):
    publication_list = []
    while True:
      soup = bs4.BeautifulSoup(self.make_profile_request().content, 'html.parser')
      items = soup.find_all('tr', {"class": "gsc_a_tr"})
      if len(items)==1:
        if items[0].find('td', {"class": "gsc_a_e"}):
          self.all_publications_retrieved = True
          break
      publication_list += items
      self.cstart += self.pagesize
    self.publications = list(map(lambda x: self.extract_compact_publication(x), publication_list))

  def get_publications_detail(self):
    unscraped_publications = filter(lambda x: not x.detail_extracted, self.publications)
    for publication in unscraped_publications:
      # time.sleep(5)
      successful = publication.scrape()
      if not successful:
        break
    self.set_all_publications_extracted()

  def set_all_publications_extracted(self):
    checker = next(filter(lambda x: not x.detail_extracted, self.publications),None)
    if checker is None:
      self.all_publications_extracted = True
    else:
      self.all_publications_extracted = False

  def save_data(self):
    data = self.export_json()
    with open(f'{self.data_path}/{self.authorID}.json', 'w') as f:
      json.dump(data, f)
    if self.all_publications_extracted:
      print('The data extraction was complete.')
      print(f'The extracted information is saved into the "{self.authorID}.json" file in the selected data path.')
    else:
      print('The publication detail extraction was incomplete.')
      print(f'The extracted information is saved into the "{self.authorID}.json" file in the selected data path.')
      print('We will continue to extract the detail of the remaining publications next time you try.')

  def export_json(self):
    data = {'authorID': self.authorID,
            'name': self.name,
            'image_link': self.image_link,
            'interests': self.interests,
            'citations': self.citations,
            'hindex': self.hindex,
            'i10index': self.i10index,
            'citation_histogram': self.citation_histogram,
            'coauthors': self.coauthors,
            'publications': [],
            'all_publications_retrieved': self.all_publications_retrieved,
            'all_publications_extracted': self.all_publications_extracted,
            'cstart': self.cstart,
            'pagesize': self.pagesize}
    data['publications'] = list(map(lambda x: x.export_json(), self.publications))
    return data

  def scrape(self):
    if not self.all_publications_retrieved:
      self.get_soup()
      self.get_full_name()
      self.get_image_link()
      self.get_interests()
      self.get_citation_metrics()
      self.get_citation_histogram()
      self.get_coauthors()
      self.get_publications_list()
    if not self.all_publications_extracted:
      self.get_publications_detail()
    self.save_data()

def create_author(authorID):
  try:
    with open(f'{DATA_PATH}/{authorID}.json', 'r') as f:
      data = json.load(f)

    publications_data = data.pop('publications')
    cstart = data.pop('cstart')
    pagesize = data.pop('page')

    author = Author(**data)
    author.get_soup()
    author.cstart = cstart
    author.pagesize = pagesize

    pubulications = list(map(lambda pub: Publication(**pub, cookies=author.cookies),
                            publications_data))
    author.publications = pubulications

    return author
  except:
    return Author(authorID)

# In[14]:


author_obj = create_author(AUTHORID)
author_obj.scrape()
author_obj.all_publications_extracted

# In[ ]:


len(list(filter(lambda x:  x.detail_extracted, author_obj.publications)))

# In[ ]:


len(author_obj.publications)


# In[ ]:




# In[ ]:



