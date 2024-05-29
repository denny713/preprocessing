# gunakan environment cuda39
# pengembangan dari test_b.py

# import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from urllib.parse import quote, unquote, urlparse, parse_qs, urlsplit, urljoin

# from bs4 import BeautifulSoup
from lxml import html

import time

import uuid
from pymongo import MongoClient 

class scrapper(object):
    def __init__(self):        
        # def create_driver():
        opt = webdriver.ChromeOptions()
        opt.add_argument('--no-sandbox') #Disables the sandbox for all process types that are normally sandboxed. Meant to be used as a browser-level switch for testing purposes only. 
        # opt.add_argument('--headless') #Run in headless mode, i.e., without a UI or display server dependencies. 
        opt.add_argument('--disable-notifications')#Disables the Web Notification and the Push APIs.
        opt.add_argument('--disable-gpu')
        opt.add_argument('--disable-3d-apis')  #Disables warning GPU stall
        self.driver = webdriver.Chrome(options=opt)#setting up webdriver and option

        connection_string = "mongodb://localhost:27017"
        client = MongoClient(connection_string)
        self.db_marketplace = client['kci_db']
        self.SCROLL_PAUSE_TIME = 3

    def close_driver(self):
        self.driver.close


class tokopedia(scrapper):
    def cari_produk(self, apa='jagung', halaman=1):
        # ob=5 adalah untuk menampilkan pencarian berdasarkan ulasan pembeli
        # rt=4 adalah untuk menampilkan rating minimal 4
        yang_dicari = quote(apa)
        
        print('mencari: ' + yang_dicari)

        if halaman==1:
            url = 'https://www.tokopedia.com/search?ob=5&rt=4&q='+yang_dicari
        else:
            url = 'https://www.tokopedia.com/search?ob=5&rt=4&page='+str(halaman)+'&q='+yang_dicari

        # content = driver.get(url + what) #target website
        content = self.driver.get(url) #target website


        delay = 3 # seconds
        # try:
        #     content_items = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='divSRPContentProducts']")))
        #     print ("Page is ready!")
        # except TimeoutException:
        #     print ("Loading took too much time!")


        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        # SCROLL_PAUSE_TIME = 0.5
        # SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(delay)
        content_items = self.driver.find_elements(By.XPATH, "//*[@class='pcv3__container css-1izdl9e']")

        nomor_halaman = self.driver.find_elements(By.XPATH, "//button[@class='css-bugrro-unf-pagination-item']")
        total_halaman = len(nomor_halaman)
        if (total_halaman>1):
            # print(total_halaman)
            halaman_terakhir = nomor_halaman[total_halaman-1].text
            temp = halaman_terakhir.split('.')
            halaman_terakhir = ''.join(temp)
            # print(type(halaman_terakhir))
            # print(halaman_terakhir)
            halaman_terakhir = int(halaman_terakhir)
        else:
            halaman_terakhir = 1

        return content_items, halaman_terakhir

    def cari_toko(self, nama_toko=''):
        url = 'https://www.tokopedia.com/' + nama_toko

        print('url toko:' + url)

        # content = driver.get(url + what) #target website
        content = self.driver.get(url) #target website


        # delay = 3 # seconds
        # try:
        #     content_items = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='divSRPContentProducts']")))
        #     print ("Page is ready!")
        # except TimeoutException:
        #     print ("Loading took too much time!")


        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        # SCROLL_PAUSE_TIME = 0.5
        # SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # time.sleep(delay)
        time.sleep(self.SCROLL_PAUSE_TIME)
        content_items = self.driver.find_elements(By.XPATH, "//*[@class='pcv3__container css-1izdl9e']")

        halaman_berikutnya = self.driver.find_elements(By.XPATH, "//a[@data-testid='btnShopProductPageNext']")
        
        # print(str(content_items))
        # print(str(halaman_berikutnya))

        item_pencarian = self.scraping(content_items, 'toko')
        # print(str(item_pencarian))

        while True:
            if (len(halaman_berikutnya)>0):
                halaman_berikutnya[0].click()

                last_height = self.driver.execute_script("return document.body.scrollHeight")

                while True:
                    # Scroll down to bottom
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.driver.execute_script("window.scrollBy(0, 800);")
                    # Wait to load page
                    time.sleep(self.SCROLL_PAUSE_TIME)

                    # Calculate new scroll height and compare with last scroll height
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                time.sleep(self.SCROLL_PAUSE_TIME)

                content_items = self.driver.find_elements(By.XPATH, "//*[@class='pcv3__container css-1izdl9e']")                
                halaman_berikutnya = self.driver.find_elements(By.XPATH, "//a[@data-testid='btnShopProductPageNext']")

                item_pencarian_list = self.scraping(content_items, 'toko')
                item_pencarian = item_pencarian + item_pencarian_list
            else:
                break
        print(item_pencarian)
        return item_pencarian

    def scraping(self, elements, kategori):
        print('data scrapping....')
        # print(elements)
        content_items = elements
        product_list = []
        no = 1
        for item in content_items:
            # print("No: " + str(no))
            # print(item.get_attribute('innerHTML'))
            # print(item)
            # print('\n')
            item_str = item.get_attribute('innerHTML')
            item_html = html.fromstring(item_str)
            img = item_html.xpath('//img')
            item_img = img[0].get('src')
            item_img_url_unquote = unquote(item_img)
            item_img_url = item_img_url_unquote
            # print(item_img_url_unquote)

            detail = item_html.xpath('//a[@class="pcv3__info-content css-gwkf0u"]')
            item_url = detail[0].get('href')
            # print(item_url)
            item_url_unquote = unquote(item_url)
            parsed_url = urlparse(item_url_unquote)
            item_url_parse_qs = parse_qs(parsed_url.query)
            r = item_url_parse_qs.get('r')
            if str(type(r)) == "<class 'list'>":
                if len(r)>0:
                    item_url = r[0]

            item_url = urljoin(item_url, urlparse(item_url).path)
            item_review_url = item_url + '/review'

            item_title = detail[0].get('title')
            price = detail[0].xpath('//div[@class="prd_link-product-price css-h66vau"]')
            item_price = price[0].text.replace('Rp','')
            temp = item_price.split('.')
            item_price = ''.join(temp)
            loc = detail[0].xpath('//span[@class="prd_link-shop-loc css-1kdc32b flip"]')
            if len(loc)>0:
                item_store_in = loc[0].text
            else:
                item_store_in = ''
            store = detail[0].xpath('//span[@class="prd_link-shop-name css-1kdc32b flip"]')
            if len(store)>0:
                item_store_name = store[0].text
            else:
                item_store_name = ''
            rating = detail[0].xpath('//span[@class="prd_rating-average-text css-t70v7i"]')
            if len(rating)>0:
                item_store_rating = rating[0].text
            else:
                item_store_rating = ''
            jml_terjual = detail[0].xpath('//span[@class="prd_label-integrity css-1sgek4h"]')
            if len(jml_terjual)>0:
                item_jml_terjual = jml_terjual[0].text
                item_jml_terjual = item_jml_terjual.split(' ')[0]
            else:
                item_jml_terjual = ''
            # print(item_store_rating)

            uid = uuid.uuid1()
            # uid = uuid.uuid4()
            item_id = uid.hex
            # product_item = [item_title, item_price, item_store_name, item_store_in, item_store_rating, item_img, item_url]
            product_item = {
                "item_id" : item_id,
                "item_kategori" : kategori,
                "item_nama" : item_title,
                "item_harga" : item_price,
                "item_toko" : item_store_name,
                "item_toko_kota" : item_store_in,
                "item_rating" : item_store_rating,
                "item_terjual" : item_jml_terjual,
                "item_img_url" : item_img_url,
                "item_url" : item_url,
                "item_review_url" : item_review_url
            }
            print(product_item)

            product_list.append(product_item)

            print("\n")
            no = no + 1
        
        return product_list

    def delete_pencarian(self, apa):
        query = { "item_kategori": apa }
        # self.db_marketplace.tokped.delete_one(query)
        self.db_marketplace.tokopedia.delete_one(query)

    def simpan_ke_tabel(self, hasil_pencarian):
        new_product_list = map(dict, set(tuple(x.items()) for x in hasil_pencarian))
        print(new_product_list)
        # self.db_marketplace.tokped.insert_many(new_product_list)
        self.db_marketplace.tokopedia.insert_many(new_product_list)

    def scrap_produk(self, apa):
        halaman = 1
        # hasil_pencarian = []
        # driver = create_driver()
        print('proses mencari...')
        pencarian, jml_halaman = self.cari_produk(apa,1)
        item_pencarian = self.scraping(pencarian, apa)
        # hasil_pencarian.append(item_pencarian)
        # hasil_pencarian = hasil_pencarian + item_pencarian
        hasil_pencarian = item_pencarian
        if (jml_halaman>halaman):
            no = 2
            while no < 4:
                print('Melanjutkan pencarian halaman: ' + str(no))
                pencarian, jml_halaman = self.cari_produk(apa,no)
                item_pencarian = self.scraping(pencarian, apa)
                # hasil_pencarian.append(item_pencarian)
                hasil_pencarian = hasil_pencarian + item_pencarian
                no = no + 1

        # driver.close()
        # close_driver()
        # print(hasil_pencarian)

        # self.simpan_ke_tabel(hasil_pencarian)
        return hasil_pencarian

    def scrap_toko(self, apa):
        daftar_komentar = []
        daftar_produk = self.cari_toko(apa)
        if (len(daftar_produk)>0):
            daftar_komentar = self.scrap_komentar_hasil_pencarian(daftar_produk)
            # print(daftar_komentar)
            # self.simpan_ke_tabel(daftar_komentar)
        return daftar_komentar
            
    def muat_halaman_komentar(self, url):
        content = self.driver.get(url) #target website

        # SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(self.SCROLL_PAUSE_TIME)
        content_items = self.driver.find_elements(By.XPATH, "//*[@class='css-1k41fl7']")

        return content_items

    # def scrap_komentar(self, id_item, content_items):
    def scrap_komentar(self, produk, content_items):
        komentar_list = []
        for item in content_items:
            item_str = item.get_attribute('innerHTML')
            # print(item_str)
            # print('\n')
            item_html = html.fromstring(item_str)
            el_bintang = item_html.xpath('//div[@data-testid="icnStarRating"]')
            # print(el_bintang[0])
            temp = el_bintang[0].get('aria-label').split(' ')
            bintang = temp[-1]
            el_nama = item_html.xpath('//span[@class="name"]')
            # print(el_nama[0])
            nama = el_nama[0].text
            el_ulasan = item_html.xpath('//span[@data-testid="lblItemUlasan"]')
            # print(el_nama[0])
            if (len(el_ulasan)>0):
                ulasan = el_ulasan[0].text
            else:
                ulasan = ''
            # print('\n')

            print('bintang: ' + bintang + ' nama: ' + nama + ' ulasan: ' + ulasan + '\n')

            id_item = produk['item_id']

            # komentar_produk = {
            komentar = {
                "item_id" : id_item,
                "nama" : nama,
                "bintang" : bintang,
                "komentar" : ulasan
            }

            komentar_produk = produk | komentar
            komentar_list.append(komentar_produk)
    
        return komentar_list
    
    def scrap_komentar_hasil_pencarian(self, hasil_pencarian):
        daftar_komentar = []
        for hasil in hasil_pencarian:
            # print(hasil)
            # id_item = hasil['item_id']
            item_review_url = hasil['item_review_url']

            try:
                dom_komentar = self.muat_halaman_komentar(item_review_url)
                # print('dom komentar: ' . str(dom_komentar))

                next_halaman = '';
                if (len(dom_komentar)>0):
                    prev_next_halaman = dom_komentar[0].find_elements(By.XPATH, "//button[@class='css-16uzo3v-unf-pagination-item']")
                    if (len(prev_next_halaman)>0):
                        next_halaman = prev_next_halaman[-1]
                    nomor_halaman = dom_komentar[0].find_elements(By.XPATH, "//button[@class='css-bugrro-unf-pagination-item']")
                
                print('Jumlah halaman: ' + str(nomor_halaman) + '\n')

                # ulasan_produk = self.scrap_komentar(id_item, dom_komentar)
                ulasan_produk = self.scrap_komentar(hasil, dom_komentar)
                if len(ulasan_produk)>0:
                    # daftar_komentar.append(ulasan_produk)
                    daftar_komentar = daftar_komentar + ulasan_produk

                if len(nomor_halaman)>0:
                    halaman_terakhir = nomor_halaman[-1]
                    # print(halaman_terakhir.get_attribute('innerHTML'))
                    # print(halaman_terakhir.get_attribute('outerHTML'))
                    status = halaman_terakhir.get_attribute('data-active')
                    # print('status: ' + str(status))
                    # print(next_halaman.get_attribute('outerHTML'))
                    # while status == 'false':
                    while True:
                        print('click next halaman')
                        next_halaman.click()
                        time.sleep(self.SCROLL_PAUSE_TIME)
        
                        dom_komentar = self.driver.find_elements(By.XPATH, "//*[@class='css-1k41fl7']")
                        # ulasan_produk = self.scrap_komentar(id_item, dom_komentar)
                        ulasan_produk = self.scrap_komentar(hasil, dom_komentar)
                        if len(ulasan_produk)>0:
                            # daftar_komentar.append(ulasan_produk)
                            daftar_komentar = daftar_komentar + ulasan_produk

                        prev_next_halaman = dom_komentar[0].find_elements(By.XPATH, "//button[@class='css-16uzo3v-unf-pagination-item']")
                        next_halaman = prev_next_halaman[-1]
                        nomor_halaman = dom_komentar[0].find_elements(By.XPATH, "//button[@class='css-bugrro-unf-pagination-item']")
                        halaman_terakhir = nomor_halaman[-1]
                        status = halaman_terakhir.get_attribute('data-active')
                        if status=='true':
                            print('sudah akhir bro')
                            break
            except:
                print('error loading halaman')
                
        return daftar_komentar

    def total_halaman_pencarian(self,apa):
        pencarian, jml_halaman = self.cari_produk(apa)
        # print(pencarian)
        return jml_halaman


class bukalapak(scrapper):
    def cari_produk(self, apa='jagung', halaman=1):
    # def search(what='jagung', page=1, driver=webdriver):
        # ob=5 adalah untuk menampilkan pencarian berdasarkan ulasan pembeli
        search_in = quote(apa)
        
        print('mencari: ' + search_in)
        
        # https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D=jagung%20manis&search_source=omnisearch_keyword&source=navbar
        
        if halaman==1:
            url = 'https://www.bukalapak.com/products?search[keywords]='+search_in
        else:
            url = 'https://www.bukalapak.com/products?search[keywords]='+search_in+'&page='+str(halaman)

        # content = driver.get(url + what) #target website
        content = self.driver.get(url) #target website


        delay = 3 # seconds
        # try:
        #     content_items = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='divSRPContentProducts']")))
        #     print ("Page is ready!")
        # except TimeoutException:
        #     print ("Loading took too much time!")


        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        # SCROLL_PAUSE_TIME = 0.5
        SCROLL_PAUSE_TIME = 4

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(delay)
        content_items = self.driver.find_elements(By.XPATH, "//*[@class='bl-flex-item mb-8']")

        halaman_terakhir = 0
        nomor_halaman = self.driver.find_elements(By.XPATH, "//ul[@class='bl-pagination__list']")
        if len(nomor_halaman):
            halaman = nomor_halaman[0].find_elements(By.XPATH, "//a[@class='bl-pagination__link']")
            if len(halaman):
                # print('\njumlah halaman: ' + str(len(halaman)) + '\n')
                halaman_terakhir = halaman[len(halaman)-1].text
                # print('\nhalaman_terakhir: ' + halaman_terakhir + '\n')
                temp = halaman_terakhir.split('.')
                halaman_terakhir = ''.join(temp)
                halaman_terakhir = int(halaman_terakhir)

        return content_items, halaman_terakhir

    def scraping(self, elements, kategori):
        print('scrapping....')
        # print(elements)
        content_items = elements
        product_list = []
        # no = 1
        for item in content_items:
            # print("No: " + str(no))
            # print(item.get_attribute('innerHTML'))
            item_str = item.get_attribute('innerHTML')
            # print(item_str)
            item_html = html.fromstring(item_str)
            img = item_html.xpath('//img[@class="bl-thumbnail--img"]')
            if len(img)>0:
                item_img = img[0].get('src')
                print(item_img)
                item_img_url_unquote = unquote(item_img)
                item_img_url = item_img_url_unquote
            else:
                item_img_url = ''

            # print(item_img_url_unquote)

            detail = item_html.xpath('//section[@class="bl-product-card-new__name"]')
            # item_url = detail[0].get('href')
            detail_link = detail[0].xpath('//a[@class="bl-link"]')
            if len(detail_link)>0:
                item_url = detail_link[0].get('href')
                # item_title = detail_link[0].get_attribute('innerHTML')
                item_title = detail_link[0].text
                # print('item_url: ' + item_url)
                item_url_unquote = unquote(item_url)
                parsed_url = urlparse(item_url_unquote)
                item_url_parse_qs = parse_qs(parsed_url.query)
                r = item_url_parse_qs.get('r')
                if str(type(r)) == "<class 'list'>":
                    if len(r)>0:
                        item_url = r[0]
                item_url = urljoin(item_url, urlparse(item_url).path)
            else:
                item_url = ''
                item_title = ''

            item_review_url = item_url

            # item_title = detail[0].get('title')
            # price = detail[0].xpath('//section[@class="bl-product-card-new__prices"]')
            price = detail[0].xpath('//p[@class="bl-text bl-text--semi-bold bl-text--ellipsis__1 bl-product-card-new__price"]')
            if len(price)>0:
                item_price = price[0].text
                temp = item_price.split('.')
                item_price = ''.join(temp)
            else:
                item_price = 0
            # print('harga barang: ' + str(item_price))

            nama_toko_dan_kota = detail[0].xpath('//div[@class="bl-product-card-new__store-name-and-location"]')
            if len(nama_toko_dan_kota)>0:
                loc = nama_toko_dan_kota[0].xpath('//p[@class="bl-text bl-text--caption-12 bl-text--secondary bl-text--ellipsis__1 bl-product-card-new__store-location"]')
                if len(loc)>0:
                    item_store_in = loc[0].text
                else:
                    item_store_in = ''
                # print('lokasi toko: ' + str(item_store_in))
                
                store = nama_toko_dan_kota[0].xpath('//a[@class="bl-link"]')
                if len(store)>0:
                    item_store_name = store[0].text
                    item_store_url = store[0].get('href')
                else:
                    item_store_name = ''
                    item_store_url = ''
            else:
                item_store_in = ''
                item_store_name = ''
                item_store_url = ''
            # print('nama toko: ' + item_store_name + ' kota: ' + item_store_in + ' url toko: ' + item_store_url)

            rating = detail[0].xpath('//div[@class="bl-product-card-new__star"]')
            if len(rating)>0:
                detail_rating = detail[0].xpath('//a[@class="bl-link"]')
                if len(detail_rating)>0:
                    item_store_rating = detail_rating[0].text
                else:
                    item_store_rating = ''
            else:
                item_store_rating = ''
            # print(item_store_rating)

            uid = uuid.uuid1()
            # uid = uuid.uuid4()
            item_id = uid.hex
            # product_item = [item_title, item_price, item_store_name, item_store_in, item_store_rating, item_img, item_url]
            product_item = {
                "item_id" : item_id,
                "item_kategori" : kategori,
                "item_nama" : item_title,
                "item_harga" : item_price,
                "item_toko" : item_store_name,
                "item_toko_kota" : item_store_in,
                "item_rating" : item_store_rating,
                "item_img_url" : item_img_url,
                "item_url" : item_url,
                "item_review_url" : item_review_url
            }
            # print(product_item)

            product_list.append(product_item)

            # print("\n")
            # no = no + 1
        
        return product_list

    def delete_pencarian(self, apa):
        query = { "item_kategori": apa }
        # self.db_marketplace.tokped.delete_one(query)
        self.db_marketplace.bukalapak.delete_one(query)

    def simpan_ke_tabel(self, hasil_pencarian):
        new_product_list = map(dict, set(tuple(x.items()) for x in hasil_pencarian))
        # print(new_product_list)

        try:
            x = self.db_marketplace.bukalapak.delete_many({})
            print(str(x.deleted_count) + ' dokumen telah dihapus')
        # except:
            # print('Tabel masih kosong')
        finally:
            print('Proses menyimpan data..')
            self.db_marketplace.bukalapak.insert_many(new_product_list)

    def muat_halaman_komentar(self, url):
        content = self.driver.get(url) #target website

        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            print('Last_height, new_heigt', last_height, new_height)
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(SCROLL_PAUSE_TIME)
        content_items = self.driver.find_elements(By.XPATH, "//div[@id='section-ulasan-barang']")

        return content_items

    def scrap_komentar(self, produk, content_items):
        komentar_list = []
        for item in content_items:
            item_str = item.get_attribute('innerHTML')
            # print(item_str)
            # print('\n')
            item_html = html.fromstring(item_str)
            el_bintang = item_html.xpath('//div[@data-testid="icnStarRating"]')
            # print(el_bintang[0])
            temp = el_bintang[0].get('aria-label').split(' ')
            bintang = temp[-1]
            el_nama = item_html.xpath('//span[@class="name"]')
            # print(el_nama[0])
            nama = el_nama[0].text
            el_ulasan = item_html.xpath('//span[@data-testid="lblItemUlasan"]')
            # print(el_nama[0])
            if (len(el_ulasan)>0):
                ulasan = el_ulasan[0].text
            else:
                ulasan = ''
            # print('\n')

            print('bintang: ' + bintang + ' nama: ' + nama + ' ulasan: ' + ulasan + '\n')

            id_item = produk['item_id']

            # komentar_produk = {
            komentar = {
                "item_id" : id_item,
                "nama" : nama,
                "bintang" : bintang,
                "komentar" : ulasan
            }

            komentar_produk = produk | komentar
            komentar_list.append(komentar_produk)

        return komentar_list

    def scrap_komentar_hasil_pencarian(self, hasil_pencarian):
        # daftar_komentar = []
        komentar_list = []
        for hasil in hasil_pencarian:
            # print(hasil)
            produk = hasil
            id_item = hasil['item_id']
            item_nama = hasil['item_nama']
            item_url = hasil['item_url']
            print('\nitem_url: ' + item_url)

            # memuat url produk dan mengambil ulasan produk
            dom_komentar = self.muat_halaman_komentar(item_url)

            if len(dom_komentar)>0:
                # print('dom komentar: ' + dom_komentar[0].get_attribute('innerHTML'))
                daftar_komentar = dom_komentar.find_elements(By.XPATH, "//div[@class='c-reviews-item']")
                daftar_halaman = dom_komentar.find_elements(By.XPATH, "//a[contains(@class,'c-pagination__link')]")
                
                if len(daftar_halaman)>0:
                    print('daftar halaman: ', daftar_halaman)
                    while True:
                        for komentar in daftar_komentar[0]:
                            judul_komentar = komentar.find_elements(By.XPATH, "//h4[@class='c-reviews-item__title u-mrgn-top--1']")
                            if len(judul_komentar)>0:
                                str_judul_komentar = judul_komentar[0].text.title()
                                # str_judul_komentar = str_judul_komentar.title()
                            else:
                                str_judul_komentar = ''

                            tgl_komentar = komentar.find_elements(By.XPATH, "//p[@class='c-reviews-item__date u-fg--ash']")
                            if len(tgl_komentar)>0:
                                str_tgl_komentar = tgl_komentar[0].text
                                str_tgl_komentar = str_tgl_komentar.replace('Ditulis ', '')
                            else:
                                str_tgl_komentar = ''

                            konten_komentar = komentar.find_elements(By.XPATH, "//p[@data-testid='content']")
                            if len(konten_komentar)>0:
                                str_konten_komentar = konten_komentar[0].text
                            else:
                                str_konten_komentar = ''

                            pembuat_komentar = komentar.find_elements(By.XPATH, "//span[@data-testid='reviewer-name']")
                            if len(pembuat_komentar)>0:
                                str_pembuat_komentar = pembuat_komentar[0].text
                            else:
                                str_pembuat_komentar = ''

                            komentar_pembeli = str_judul_komentar + '::' + str_konten_komentar                        

                            komentar = {
                                "item_id" : id_item,
                                "nama" : str_pembuat_komentar,
                                # "bintang" : bintang,
                                "komentar" : komentar_pembeli,
                                "tgl_komentar" : str_tgl_komentar
                            }

                            komentar_produk = produk | komentar
                            komentar_list.append(komentar_produk)

                            tombol_prev_next = dom_komentar.find_elements(By.XPATH, "//a[@class='c-pagination__btn']")
                            if len(tombol_prev_next)>0:
                                # tombol_next = tombol_prev_next[1].get_attribute('class')
                                tombol_next = tombol_prev_next[1]
                                tombol_next_disable = tombol_next.get_attribute('disabled')
                                print('\ntombol_next_disable: ' + str(tombol_next_disable))



            else:
                print('\nTidak ada ulasan untuk produk ' + item_nama + '\n')
                
        return komentar_list

    def total_halaman_pencarian(self,apa):
        pencarian, jml_halaman = self.cari_produk(apa)
        # print(pencarian)
        return jml_halaman

class shopee(scrapper):
    def cari_produk(self, apa='jagung', halaman=1):
    # def search(what='jagung', page=1, driver=webdriver):
        # ob=5 adalah untuk menampilkan pencarian berdasarkan ulasan pembeli
        search_in = quote(apa)
        
        print('mencari: ' + search_in)
        
        # https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D=jagung%20manis&search_source=omnisearch_keyword&source=navbar
        
        if halaman==1:
            url = 'https://shopee.co.id/search?keyword=='+search_in
        else:
            url = 'https://shopee.co.id/search?keyword=='+search_in+'&page='+str(halaman)

        # content = driver.get(url + what) #target website
        content = self.driver.get(url) #target website


        delay = 3 # seconds
        # try:
        #     content_items = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='divSRPContentProducts']")))
        #     print ("Page is ready!")
        # except TimeoutException:
        #     print ("Loading took too much time!")


        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        # SCROLL_PAUSE_TIME = 0.5
        SCROLL_PAUSE_TIME = 4

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(delay)
        content_items = self.driver.find_elements(By.XPATH, "//ul[@class='row shopee-search-item-result__items']")

        halaman_terakhir = 0
        nomor_halaman = self.driver.find_elements(By.XPATH, "//span[@class='shopee-mini-page-controller__total']")
        if len(nomor_halaman):
            halaman_terakhir = nomor_halaman.text

        return content_items, halaman_terakhir

    def scraping(self, elements, kategori):
        print('scrapping....')
        # print(elements)
        content_items = elements
        product_list = []
        # no = 1
        for item in content_items:
            # print("No: " + str(no))
            # print(item.get_attribute('innerHTML'))
            item_str = item.get_attribute('innerHTML')
            # print(item_str)
            item_html = html.fromstring(item_str)
            img = item_html.xpath('//img[@class="QPVlig wOiuiE"]')
            if len(img)>0:
                item_img = img[0].get('src')
                print(item_img)
                item_img_url_unquote = unquote(item_img)
                item_img_url = item_img_url_unquote
            else:
                item_img_url = ''

            # print(item_img_url_unquote)

            # item_url = detail[0].get('href')
            detail_link = item_html.xpath('//a[@data-sqe="link"]')
            if len(detail_link)>0:
                item_url = detail_link[0].get('href')
                # item_url_unquote = unquote(item_url)
                # parsed_url = urlparse(item_url_unquote)
                # item_url_parse_qs = parse_qs(parsed_url.query)
            else:
                item_url = ''
                
            item_review_url = item_url

            detail = item_html.xpath('//div[@class="_01SYKk zL3Azb uR5B0O"]')
            if len(detail)>0:
                item_title = detail[0].text
            else:
                item_title = ''


            # item_title = detail[0].get('title')
            # price = detail[0].xpath('//section[@class="bl-product-card-new__prices"]')
            price = item_html.xpath('//span[@class="H86kR1"]')
            if len(price)>0:
                item_price = price[0].text
                temp = item_price.split('.')
                item_price = ''.join(temp)
            else:
                item_price = 0
            # print('harga barang: ' + str(item_price))
                
            # nama toko di shopee tidak ditampilkan di hasil pencarian barang
            # rating tidak ditampilkan dalam nomor

            # loc = nama_toko_dan_kota[0].xpath('//span[@aria-label="from"]')
            loc = item_html.xpath('//div[@class="iMriCi"]')
            if len(loc)>0:
                item_store_in = loc[0].text
            else:
                item_store_in = ''
            # print('lokasi toko: ' + str(item_store_in))

            uid = uuid.uuid1()
            # uid = uuid.uuid4()
            item_id = uid.hex
            # product_item = [item_title, item_price, item_store_name, item_store_in, item_store_rating, item_img, item_url]
            product_item = {
                "item_id" : item_id,
                "item_kategori" : kategori,
                "item_nama" : item_title,
                "item_harga" : item_price,
                # "item_toko" : item_store_name,
                "item_toko_kota" : item_store_in,
                # "item_rating" : item_store_rating,
                "item_img_url" : item_img_url,
                "item_url" : item_url,
                "item_review_url" : item_review_url
            }
            # print(product_item)

            product_list.append(product_item)

            # print("\n")
            # no = no + 1
        
        return product_list

    def delete_pencarian(self, apa):
        query = { "item_kategori": apa }
        # self.db_marketplace.tokped.delete_one(query)
        self.db_marketplace.shopee.delete_one(query)

    def simpan_ke_tabel(self, hasil_pencarian):
        new_product_list = map(dict, set(tuple(x.items()) for x in hasil_pencarian))
        # print(new_product_list)

        try:
            x = self.db_marketplace.shopee.delete_many({})
            print(str(x.deleted_count) + ' dokumen telah dihapus')
        # except:
            # print('Tabel masih kosong')
        finally:
            print('Proses menyimpan data..')
            self.db_marketplace.shopee.insert_many(new_product_list)

    def muat_halaman_komentar(self, url):
        content = self.driver.get(url) #target website

        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, 800);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            print('Last_height, new_heigt', last_height, new_height)
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(SCROLL_PAUSE_TIME)
        # content_items = self.driver.find_elements(By.XPATH, "//div[@id='product-ratings__list']")
        content_items = self.driver.find_elements(By.XPATH, "//div[@id='shopee-product-comment-list']")

        return content_items

    def scrap_komentar(self, produk, content_items):
        komentar_list = []
        for item in content_items:
            item_str = item.get_attribute('innerHTML')
            # print(item_str)
            # print('\n')
            item_html = html.fromstring(item_str)
            komentar = item_html.xpath('//div[@class="shopee-product-rating__main"]')
            if len(komentar)>0:
                el_nama = item_html.xpath('//a[@class="shopee-product-rating__author-name"]')
                if (len(el_nama)>0):
                    nama = el_nama[0].text
                else:
                    nama = ''
                    
                el_waktu = item_html.xpath('//div[@class="shopee-product-rating__time"]')
                if (len(el_waktu)>0):
                    waktu = el_waktu[0].text
                else:
                    waktu = ''

                el_ulasan = item_html.xpath('//div[not(@class)]')
                # print(el_nama[0])
                ulasan = ''
                if (len(el_ulasan)>0):
                    for el_detail_ulasan in el_ulasan:
                        ulasan = ulasan + ' ' + el_detail_ulasan.text
                # print('\n')

                print('bintang: ' + bintang + ' nama: ' + nama + ' ulasan: ' + ulasan + '\n')

                id_item = produk['item_id']

                # komentar_produk = {
                komentar = {
                    "item_id" : id_item,
                    "nama" : nama,
                    # "bintang" : bintang,
                    "waktu" : waktu,
                    "komentar" : ulasan
                }

                komentar_produk = produk | komentar
                komentar_list.append(komentar_produk)

        return komentar_list

    def scrap_komentar_hasil_pencarian(self, hasil_pencarian):
        # daftar_komentar = []
        komentar_list = []
        for hasil in hasil_pencarian:
            # print(hasil)
            produk = hasil
            id_item = hasil['item_id']
            item_nama = hasil['item_nama']
            item_url = hasil['item_url']
            print('\nitem_url: ' + item_url)

            # memuat url produk dan mengambil ulasan produk
            dom_komentar = self.muat_halaman_komentar(item_url)

            if len(dom_komentar)>0:
                # print('dom komentar: ' + dom_komentar[0].get_attribute('innerHTML'))
                daftar_komentar = dom_komentar.find_elements(By.XPATH, '//div[@class="shopee-product-rating__main"]')
                daftar_halaman = dom_komentar.find_elements(By.XPATH, "//div[contains(@class,'c-pagination__link')]")
                
                # if len(daftar_halaman)>0:
                if len(daftar_komentar)>0:
                    print('daftar halaman: ', daftar_halaman)
                    while True:
                        for komentar in daftar_komentar[0]:
                            tgl_komentar = komentar.find_elements(By.XPATH, "//div[@class='shopee-product-rating__time']")
                            if len(tgl_komentar)>0:
                                str_tgl_komentar = tgl_komentar[0].text
                                str_tgl_komentar = str_tgl_komentar.replace('Ditulis ', '')
                            else:
                                str_tgl_komentar = ''

                            str_konten_komentar = ''
                            konten_komentar = komentar.find_elements(By.XPATH, "//div[not(@class)]")
                            if len(konten_komentar)>0:
                                # str_konten_komentar = konten_komentar[0].text
                                for detail_komentar in konten_komentar:
                                    str_konten_komentar = str_konten_komentar  + ' ' + detail_komentar.text

                            pembuat_komentar = komentar.find_elements(By.XPATH, "//a[@class='shopee-product-rating__author-name']")
                            if len(pembuat_komentar)>0:
                                str_pembuat_komentar = pembuat_komentar[0].text
                            else:
                                str_pembuat_komentar = ''

                            komentar_pembeli = str_konten_komentar                        

                            komentar = {
                                "item_id" : id_item,
                                "nama" : str_pembuat_komentar,
                                # "bintang" : bintang,
                                "komentar" : komentar_pembeli,
                                "tgl_komentar" : str_tgl_komentar
                            }

                            komentar_produk = produk | komentar
                            komentar_list.append(komentar_produk)

                            tombol_prev_next = dom_komentar.find_elements(By.XPATH, "//button[@class='shopee-icon-button shopee-icon-button--right']")
                            if len(tombol_prev_next)>0:
                                # tombol_next = tombol_prev_next[1].get_attribute('class')
                                tombol_next = tombol_prev_next[1]
                                tombol_next_disable = tombol_next.get_attribute('disabled')
                                print('\ntombol_next_disable: ' + str(tombol_next_disable))



            else:
                print('\nTidak ada ulasan untuk produk ' + item_nama + '\n')
                
        return komentar_list

    def total_halaman_pencarian(self,apa):
        pencarian, jml_halaman = self.cari_produk(apa)
        # print(pencarian)
        return jml_halaman
