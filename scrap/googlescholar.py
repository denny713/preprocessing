import bs4
import requests
import re


def scrape_google_scholar(author_id):
    author_detail = author(author_id)
    print(author_detail)
    return []


def author(id):
    all_publications_retrieved = False
    all_publications_extracted = False
    cookies = None
    page_start = 0
    page_size = 100
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    url = f"https://scholar.google.com/citations?hl=en&user={id}&cstart={page_start}&pagesize={page_size}"
    response = requests.request("GET", url, headers=headers, cookies=None)

    if response.status_code == 429:
        raise Exception("The server responded with Error 429. We have been detected. Wait before trying again.")
        return None

    full_name = ""
    image_link = ""
    interests = ""
    citations = ""
    hindex = ""
    i10index = ""
    citation_histogram = ""
    coauthors = ""
    publications = []

    cookies = response.cookies
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    name = soup.find('div', {'id': 'gsc_prf_in'})
    if name:
        full_name = name.get_text()

    image = soup.find('div', {'img': 'gsc_prf_pup-img'})
    if image:
        image_link = image.get('src')

    interests = list(map(lambda x: x.get_text(), soup.find_all('a', {'class': 'gsc_prf_inta'})))

    citation_info = soup.find('div', {'id': 'gsc_rsb_cit'})
    citation = citation_info.find('a', text=re.compile('Citations'), attrs={'class': 'gsc_rsb_f'})
    if citation:
        citation_value = citation.parent.parent.find_all('td', {'class': 'gsc_rsb_std'})
        if len(citation_value) > 0:
            citations = int(citation_value[0].get_text())

    hindex = citation_info.find('a', text=re.compile('h-index'), attrs={'class': 'gsc_rsb_f'})
    if hindex:
        hindex_value = hindex.parent.parent.find_all('td', {'class': 'gsc_rsb_std'})
        if len(hindex_value) > 0:
            hindex = int(hindex_value[0].get_text())

    i10index = citation_info.find('a', text=re.compile('i10-index'), attrs={'class': 'gsc_rsb_f'})
    if i10index:
        i10index_value = i10index.parent.parent.find_all('td', {'class': 'gsc_rsb_std'})
        if len(i10index_value) > 0:
            i10index = int(i10index_value[0].get_text())

    citation_hist = soup.find_all('div', {'class': 'gsc_md_hist_w'})
    if citation_hist:
        citation_hist = citation_hist[0]
        citation_hist_time = list(map(lambda x: x.get_text(), citation_hist.find_all('span', {'class': 'gsc_g_t'})))
        citation_hist_cites = list(map(lambda x: x.get_text(), citation_hist.find_all('a', {'class': 'gsc_g_a'})))
        citation_histogram = list(zip(citation_hist_time, citation_hist_cites))

    coauthor_list = soup.find('div', {'id': 'gsc_rsb_co'})
    if coauthor_list:
        if coauthor_list.find('button'):
            coauthor_list = bs4.BeautifulSoup(response.content, 'html.parser').find('div', {
                'id': 'gsc_codb_content'})
            coauthor_list = coauthor_list.find_all('div', {'class': 'gsc_ucoar'})
            coauthor_ids = list(map(lambda x: x.get('id').split('-')[-1], coauthor_list))
            coauthor_names = list(map(lambda x: x.find('img').get('alt'), coauthor_list))
            coauthors = list(zip(coauthor_ids, coauthor_names))
        else:
            coauthor_list = coauthor_list.find_all('img')
            coauthor_ids = list(map(lambda x: x.get('id').split('-')[1], coauthor_list))
            coauthor_names = list(map(lambda x: x.get('alt'), coauthor_list))
            coauthors = list(zip(coauthor_ids, coauthor_names))

    publication_list = []
    while True:
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('tr', {"class": "gsc_a_tr"})
        print("Items: ", items)
        if len(items) == 1:
            if items[0].find('td', {"class": "gsc_a_e"}):
                all_publications_retrieved = True
                break
        publication_list += items
        page_start += page_size
    publications = list(map(lambda x: extract_publication(x), publication_list))

    unscraped_publications = filter(lambda x: not x.detail_extracted, publications)
    for publication in unscraped_publications:
        successful = publication.scrape()
        if not successful:
            break
    checker = next(filter(lambda x: not x.detail_extracted, publications), None)
    if checker is None:
        all_publications_extracted = True
    else:
        all_publications_extracted = False

    print("Full name:", full_name)
    print("Image link:", image_link)
    print("Interests:", interests)
    print("Citations:", citations)
    print("H-index:", hindex)
    print("i10-index:", i10index)
    print("Citation Histogram:", citation_histogram)
    print("Coauthors:", coauthors)
    print("Publications:", publications)

    return {'authorID': id, 'name': name, 'image_link': image_link, 'interests': interests, 'citations': citations,
            'hindex': hindex, 'i10index': i10index, 'citation_histogram': citation_histogram, 'coauthors': coauthors,
            'publications': list(map(lambda x: extract_publication(x), publications)),
            'all_publications_retrieved': all_publications_retrieved,
            'all_publications_extracted': all_publications_extracted, 'cstart': page_start, 'pagesize': page_size}


def extract_publication(publication_element):
    title = publication_element.find('a', {"class": "gsc_a_at"}).get_text()
    year = publication_element.find('td', {"class": "gsc_a_y"}).find('span', {"class": "gsc_a_hc"}).get_text()
    if year:
        year = int(year)
    else:
        year = None
    url = publication_element.find('a', {"class": "gsc_a_at"}).get('href').split('?')[-1]
    cited_by = publication_element.find('a', {"class": "gsc_a_ac"}).get_text()
    if cited_by:
        cited_by = int(cited_by)
    else:
        cited_by = None
    return publication(title, year, cited_by, url=url, cookies=None)


def publication(title, year, cited_by, url, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    uri = f'https://scholar.google.com/citations?{url}'
    response = requests.request("GET", uri, headers=headers, cookies=cookies)

    detail_extracted = False
    if response.status_code == 200:
        detail_extracted = True

    soup = bs4.BeautifulSoup(response.content, 'lxml')

    link = ""
    authors = ""
    desc = ""
    citation_histogram = ""

    title = soup.find('div', {'id': 'gsc_oci_title'})
    if title:
        link = title.find('a', {'class': 'gsc_oci_title_link'})
        if link:
            link = link.get('href')

    authors = soup.find('div', text=re.compile('Authors'), attrs={'class': 'gsc_oci_field'})
    if authors:
        authors = authors.parent.find('div', {'class': 'gsc_oci_value'}).get_text().split(', ')
    else:
        inventors = soup.find('div', text=re.compile('Inventors'), attrs={'class': 'gsc_oci_field'})
        if inventors:
            authors = inventors.parent.find('div', {'class': 'gsc_oci_value'}).get_text().split(', ')

    description = soup.find('div', {'id': 'gsc_oci_descr'})
    if description:
        desc = description.get_text()

    citation_hist = soup.find('div', {'id': 'gsc_oci_graph_bars'})
    if citation_hist:
        citation_hist_time = list(
            map(lambda x: int(x.get_text()), citation_hist.find_all('span', {'class': 'gsc_oci_g_t'})))
        citation_hist_cites = list(
            map(lambda x: int(x.get_text()), citation_hist.find_all('span', {'class': 'gsc_oci_g_al'})))
        citation_histogram = list(zip(citation_hist_time, citation_hist_cites))

    print("Link: ", link)
    print("Authors: ", authors)
    print("Description: ", desc)
    print("Citation Histogram: ", citation_histogram)

    return {
        'url': uri,
        'title': title,
        'link': link,
        'year': year,
        'cited_by': cited_by,
        'authors': authors,
        'description': desc,
        'citation_histogram': citation_histogram,
        'detail_extracted': detail_extracted
    }
