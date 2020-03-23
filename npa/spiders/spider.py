import scrapy
import uuid
import pymongo
import json
from time import sleep
from urllib.parse import urlparse, parse_qs, urlencode
from ..items import NpaItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    count_for = 0
    count_detail = 0
    source_tmb_count = 0 
    source_ktb_count = 0
    client = pymongo.MongoClient("mongodb://npaDB:npaadmin@cluster0-shard-00-00-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-01-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-02-ipibu.gcp.mongodb.net:27017/npaWebAppDB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.get_default_database()
    collection = db['scrap_elem']
    taget_source = collection.find()
    # url_list = []
    # for elem in taget_source:
    #    url_list.append(elem['url']) 

    # start_urls = url_list #property list page url   

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        # self.driver = webdriver.Chrome(executable_path="../chromedriver", chrome_options=self.chrome_options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.chrome_options)
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path='/usr/bin/chromedriver') 

# demo.pyimport scrapyfrom selenium import webdriver
# options = webdriver.ChromeOptions()        
# options.add_argument("--disable-extensions")        
# options.add_argument("--headless")        
# options.add_argument("--disable-gpu")       
# options.add_argument("--no-sandbox")        
# self.driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')       


    def start_requests(self):
        for source in self.taget_source:
            print(source['source']+'----------------------------------------------------------------------------------------------')
            source_url = source['url']   

            self.driver.get(source_url)
            source_dict = source

            while(1):
                #get detail page url
                source = self.driver.page_source
                sel = scrapy.Selector(text=source)
                urls =  sel.xpath(source_dict['item_page']).extract()
                for url in urls: 
                    if source_dict['source'] == 'TMB':
                        self.source_tmb_count += 1 
                    elif source_dict['source'] == 'KTB':
                        self.source_ktb_count += 1

                    self.count_for +=1
                    print("for count = "+str(self.count_for))
                    if source_dict['base_url'] in url:
                        url = url
                    else:
                        url = f"{source_dict['base_url']}/{url}"
                    yield scrapy.Request(url=url, callback=self.parse_details,meta={'source_url': source_url})

                # follow pagination link
                try:
                    next_page = self.driver.find_element_by_xpath(source_dict['next_page'])
                    next_page.click()
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, source_dict['next_page'])))
                except:
                    break
       

       



    #parse detail page
    def parse_details(self, response):

        self.count_detail +=1
        print("detail parse count = " + str(self.count_detail))
    
        items = NpaItem()

        source_url = response.meta['source_url']
        source_dict = self.collection.find_one({'url' : source_url})


        _id =  source_dict['source'] + response.xpath(source_dict['asset_code']).extract_first()
        source = source_dict['source']
        url = response.url
        img = response.xpath(source_dict['img']).extract()
        gg_map = response.xpath(source_dict['gg_map']).extract()
        price = response.xpath(source_dict['price']).extract()
        asset_type = response.xpath(source_dict['asset_type']).extract()
        asset_code = response.xpath(source_dict['asset_code']).extract()
        area = response.xpath(source_dict['area']).extract()
        deed_num = response.xpath(source_dict['deed_num']).extract()
        address = response.xpath(source_dict['address']).extract()
        contact = response.xpath(source_dict['contact']).extract()
        more_detail = response.xpath(source_dict['more_detail']).extract()

        items['_id'] =  _id
        items['source'] = source
        items['url'] = url
        items['img'] = self.image_link_check(img,source_dict['base_url'])
        items['gg_map'] = gg_map
        items['price'] = price
        items['asset_type'] = asset_type
        items['asset_code'] = asset_code
        items['area'] = area
        items['deed_num'] = deed_num
        items['address'] = address
        items['contact'] = contact
        items['more_detail'] = more_detail

        print("TMB" + str(self.source_tmb_count))
        print("KTB" + str(self.source_ktb_count))

        yield items

    #when @scr is not absolute url link "../gallery/test.jpg"
    def image_link_check(self,img_array,base_url):
        parse = urlparse(base_url)
        domain = parse.netloc
        absolute_url = []
        for img_url in img_array:
            if domain in img_url or 'https://' in img_url:
                absolute_url.append(img_url)
            else:
                if "../" in img_url:
                    img_url =  img_url.replace("../","/")
                if base_url.split[3] in img_url:
                    if img_url[0] == '/':
                        absolute__img_url =  f"https://{domain}{img_url}"
                    else:
                        absolute__img_url =  f"https://{domain}/{img_url}"
                else:
                    if img_url[0] == '/':
                        absolute__img_url =  f"{base_url}{img_url}"
                    else:
                        absolute__img_url =  f"{base_url}/{img_url}"
                absolute_url.append(absolute__img_url)
        return absolute_url
