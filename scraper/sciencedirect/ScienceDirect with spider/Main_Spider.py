#!/usr/bin/env python
# -*- coding:utf-8 -*-
# anthor: godusevpn time:2017/12/17


import time
import url_analyse
import translate
import write_to_file
import os




# Hàm chính
class Spider:
    # Khởi tạo
    def __init__(self):
        self.url_analyse = url_analyse.Url_analyse()
        self.translate = translate.Translate()
        self.write_to_file = write_to_file.Write_to_file()



    def remove_exist_floder(self,KeyWords):
        # Remove the existing folder (named after KeyWords) 
        path = '.\\Data_tommy\\' + KeyWords
        if not os.path.exists(path):
            os.makedirs(path)




    def remove_exist_txt(self,KeyWords):
        # Remove the existing result file (named after KeyWords.txt) 
        filename = '.\\Data_tommy\\' + KeyWords + '\\' + KeyWords + '.txt'
        if os.path.exists(filename):
            os.remove(filename)
            return




    def get_start_url(self,KeyWords):
        # Use spaces to slice keywords 
        KeyWords_split = KeyWords.split()
        # Splicing start page URL 
        #            https://www.sciencedirect.com/search?qs=covid&show=25&sortBy=relevance&offset=0
        start_url = 'https://www.sciencedirect.com/search?&qs='
        for ii in range(0, len(KeyWords_split)):
            # 'http://www.sciencedirect.com/search?qs=turbine%20blade%20crack&show=25&sortBy=relevance'
            if ii == 0:
                start_url = start_url + KeyWords_split[ii]
            else:
                start_url = start_url + '%25' + KeyWords_split[ii]
        start_url = start_url + '&show=25&sortBy=relevance'
        return start_url




    def run(self,KeyWords,Page_num):
        # Remove the existing folder (named after KeyWords) 
        self.remove_exist_floder(KeyWords)

        # Remove the existing result file (named after KeyWords.txt)
        self.remove_exist_txt(KeyWords)

        # Get start page URL 
        start_url = self.get_start_url(KeyWords)

        # Analyze the starting search page 
        new_urls = self.url_analyse.analyse_SearchPage(start_url)

        # Start crawling 
        count = 1
        while True:
            print("Hoàn thành: {}/{} - {:.0f}%".format(count,Page_num,(count*100/Page_num)))
            # Take a new link from new_urls for crawling 
            if len(new_urls):
                # Take a new link from new_urls for crawling 
                new_url = new_urls[0]

                # Crawl new links to get English titles and English abstracts 
                (title_en, abstract_en) = self.url_analyse.analyse_EveryPage(new_url, count)

                 # Remove crawled links from new_urls 
                new_urls.remove(new_urls[0])

                # Use Baidu Translation API to translate titles and abstracts
                title_cn = self.translate.en2ch(title_en)
                abstract_cn = self.translate.en2ch(abstract_en)

                # Write the article information (Chinese and English title, Chinese and English abstract, PDF download link) into KeyWords.txt 
                self.write_to_file.write_to_txt(KeyWords,count,title_en,abstract_en,title_cn,abstract_cn,new_url)

                # Count the number of documents processed
                count = count + 1

            else:
                # Turn page 50 offset=50&qs=covid&show=25
                print(start_url + '&offset=' + str(int(count*25)))
                #start_url = 'http://www.sciencedirect.com/search?offset=0&qs='
                # print(start_url + '&offset=' + str(int(count-1)))
                #new_urls = self.url_analyse.analyse_SearchPage(start_url + '&offset=' + str(int(count-1)))
                new_urls = self.url_analyse.analyse_SearchPage(start_url + '&offset=' + str(int(count*25)))

            # Quit if the number of documents searched reaches the requirement 
            if count>Page_num:
                break







# Main Program
if __name__ == "__main__":

    # Instantiate the crawler
    spider = Spider()

    # The start time of the statistical procedure
    start = time.time()

    # Search keywords (method 1 assignment)
    # KeyWords = 'crack breathing rotor'

    # Search keywords (method 2 keyboard input) 
    KeyWords = input('Enter the keywords you want to find (connect with spaces): ')

    # Set the number of search articles
    Page_num = 5

    # Print search initial conditions
    print(KeyWords, Page_num)

    # Start crawling 
    spider.run(KeyWords, Page_num)
