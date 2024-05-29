#conding:utf8

import time
from bs4 import BeautifulSoup
import random

from urllib.request import urlopen
from urllib.request import Request

class Url_analyse(object):
    def __init__(self):
        self.ok = 'ok'




    # Crawl search page 
    def analyse_SearchPage(self, start_url):
        print('Search page>Crawling ' + start_url)
        req = Request(start_url)
        req.add_header("Host", "www.sciencedirect.com")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        flag = 1
        while flag<20:
            try:
                print('Search page> is sending a request to the web page')
                resp = urlopen(req, timeout=10)
                flag = 200
                soup = BeautifulSoup(resp, "html.parser")
                new_urls = []
                for ii in soup.find_all("div", {"class": "result-item-content"}):
                    for jj in ii.find_all("h2"):
                        for zzl_href in jj.find_all("a"):
                            new_urls.append(r'http://www.sciencedirect.com' + zzl_href.get('href'))

            except:
                print('Search page>The network has a problem, the %s reconnection '% str(flag))
                flag = flag +1
                new_urls = []
                if flag > 20:
                    print('Retrieve page>abandon crawling' )
        return new_urls






    # Crawl the paper page 
    def analyse_EveryPage(self, new_url, count):
        print('\n\n Page> Crawling  %d : %s' % (count, new_url))
        req = Request(new_url)
        req.add_header("Host", "www.sciencedirect.com")
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")


        flag = 1
        # Reconnect up to 20 times after failure 
        while flag<20:
            try:
                print('Thesis page> is sending a request to the web page' )
                resp = urlopen(req, timeout=10)
                flag = 200
                soup = BeautifulSoup(resp, "html.parser")
                try:
                    print('Thesis page> is parsing content from the web page')
                    title = soup.find("span", {"class": "title-text"}).get_text()
                    temp = soup.find("div", {"class": "abstract author"})
                    abstract = temp.find("p").get_text()
                except:
                    print('Thesis page>Failed to parse content from webpage' )
                    title = 'Thesis page>Parsing failed' 
                    abstract = 'Thesis page>Parsing failed' 
            except:
                print('Thesis page>There is a problem with the network, the %s reconnection' % str(flag))
                flag = flag + 1
                title = 'Thesis page>Failed to reconnect multiple times' 
                abstract = 'Thesis page>Failed to reconnect multiple times'
                if flag > 20:
                    print('Thesis page> Give up crawling')


        # Rest for a while and then climb 
        time_lapse = random.uniform(2, 4)
        print('Thesis page>Pause %f seconds to climb the next article' % (time_lapse))
        time.sleep(time_lapse)


        return (title,abstract)



