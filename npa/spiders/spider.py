import scrapy
import uuid
import pymongo
import json
import pytz
from time import sleep
from urllib.parse import urlparse, parse_qs, urlencode
from ..items import NpaItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from w3lib.html import remove_tags
from ..function.address_check import address_check
from ..function.get_time import now_string
from ..function.str_concat import str_concat, str_concat_nospace, str_concat_comma
from ..function.area_split import area_split




class SpiderSpider(scrapy.Spider):
    name = 'spider'
    # count_for = 0
    # count_detail = 0
    # source_tmb_count = 0 
    # source_ktb_count = 0
    client = pymongo.MongoClient("mongodb://npaDB:npaadmin@cluster0-shard-00-00-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-01-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-02-ipibu.gcp.mongodb.net:27017/npaWebAppDB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.get_default_database()
    collection = db['scrap_elem']
    taget_source = collection.find({'scrape':1})
    #remove all oud data
    forRemove = db['properties']
    
    for item in forRemove.find({}):
        forRemove.update({'_id':item['_id']},{'$set':{'status':1}})
        
    # try:
    #     forRemove.remove({})
    # except:
    #     print("No data in collection")
    # url_list = []
    # for elem in taget_source:
    #    url_list.append(elem['url']) 

    # start_urls = url_list #property list page url   

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        # self.driver = webdriver.Chrome(executable_path="../chromedriver", chrome_options=self.chrome_options)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.chrome_options)
        # self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path='/usr/bin/chromedriver') 

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
                    # if source_dict['source'] == 'TMB':
                    #     self.source_tmb_count += 1 
                    # elif source_dict['source'] == 'KTB':
                    #     self.source_ktb_count += 1

                    # self.count_for +=1
                    # print("for count = "+str(self.count_for))
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
            #after all spider of this source
            self.collection.update({'source':source['source']},{'$set':{'scrape':0}})
       
       

       



    #parse detail page
    def parse_details(self, response):

        # self.count_detail +=1
        # print("detail parse count = " + str(self.count_detail))
    
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
        scraping_date = self.now_string()

        items['_id'] =  _id
        items['source'] = source
        items['asset_url'] = url
        items['asset_img'] = self.image_link_check(img,source_dict['base_url'])
        try:
            items['gg_map'] = gg_map[0]
        except:
            items['gg_map'] = "Google map not found"
        items['price'] = str_concat_nospace(price).strip()
        items['asset_type'] = self.remove_space_tag(self.remove_html(str_concat_nospace(asset_type)))
        items['asset_code'] = self.remove_space_tag(self.remove_html(str_concat_nospace(asset_code)))
        items['area'] = self.remove_space_tag(self.remove_html(str_concat_nospace(area))) 
        area_dict = area_split(self.remove_space_tag(self.remove_html(str_concat_nospace(area))))
        items['area_rai'] = float(area_dict['rai'])
        items['area_ngan'] = float(area_dict['ngan'])
        items['area_sq_wa'] = float(area_dict['sq_wa'])
        items['deed_num'] = self.remove_space_tag(self.remove_html(str_concat(deed_num)))
        items['address'] = self.remove_space_tag(self.remove_html(str_concat(address))).strip()
        address_dict = address_check(items['address'])
        items['province'] = address_dict['province']
        items['district'] = address_dict['district']
        items['sub_district'] = address_dict['sub_district']

        items['contact'] =  self.remove_space_tag(self.remove_html(str_concat_comma(contact))) 
        items['more_detail'] = self.remove_space_tag(self.remove_html(str_concat(more_detail)))
        items['update_date'] = scraping_date
        items['status'] = 0
         #0=new, 1=old, 2=deleted 

        # print("TMB" + str(self.source_tmb_count))
        # print("KTB" + str(self.source_ktb_count))

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

    def now_string(self):
        now = datetime.now()
        bkk_tz = pytz.timezone('Asia/Bangkok')
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        bkk_dt = now.astimezone(bkk_tz)
        dt_string = bkk_dt.strftime(fmt)
        return dt_string

    def remove_html(self,text_data):
        cleaned_data = ''
        try:
            cleaned_data = remove_tags(text_data)
        except TypeError:
            cleaned_data = 'No data'
        return cleaned_data.strip()

    def remove_space_tag(self,text_data):
        if "\n" in text_data:
            text_data.replace('\n','')
        if "&nbsp" in text_data:
            text_data.replace('&nbsp','')
        return text_data.strip()



