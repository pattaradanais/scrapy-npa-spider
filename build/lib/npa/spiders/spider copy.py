import scrapy
import uuid
import pymongo
import json
from urllib.parse import urlparse, parse_qs, urlencode
from ..items import NpaItem


class SpiderSpider(scrapy.Spider):
    name = 'spider2'
    start_urls = [] #property list page url

    client = pymongo.MongoClient("mongodb://npaDB:npaadmin@cluster0-shard-00-00-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-01-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-02-ipibu.gcp.mongodb.net:27017/npaWebAppDB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.get_default_database()
    collection = db['scrap_elem']
    taget_source = collection.find()
   


    def start_requests(self):
        for elem in self.taget_source:
            print(elem['source']+'----------------------------------------------------------------------------------------------')
            url = elem['url']
            yield scrapy.Request(url=url, callback=self.paurse_page, meta={'source_url': url})

    #เข้าถึง DB เพื่่อนำ attr ของแต่ละ src มาดึงข้อมูล
    # def parse(self, response):
    #     print('test acess db')
    #     for elem in self.taget_source:
    #         print(elem['source']+'----------------------------------------------------------------------------------------------')
    #         url = elem['url']
    #         yield scrapy.Request(url=url, callback=self.paurse_page)
       

    #parse detail page link and next page
    def paurse_page(self, response):
        source_url = response.meta['source_url']

        source_dict = self.collection.find_one({'url' : source_url})

        if source_dict['next_page']['type'] == 'formData':
            start_page = {}
            start_page[source_dict['next_page']['path']] = source_dict['next_page']['start_page']
        if source_dict['next_page']['type'] == 'queryString':
            start_page =  source_dict['next_page']['start_page']
        
        #get detail page url
        urls =  response.xpath(source_dict['item_page']).extract()
        for url in urls:
            if source_dict['base_url'] in url:
                url = response.urljoin(url)
            else:
                url = source_dict['base_url'] + url
            yield scrapy.Request(url=url, callback=self.parse_details,meta={'source_url': source_url})

        # follow pagination link

        if source_dict['next_page']['type'] == 'url':
            next_page_url = response.xpath(source_dict['next_page']['path']).extract_first()
            print(next_page_url)
            if next_page_url:
                next_page_url = response.urljoin(next_page_url)
                yield scrapy.Request(url=next_page_url, callback=self.paurse_page,meta={'source_url': source_url})
        if source_dict['next_page']['type'] == 'formData':
            start_page[source_dict['next_page']['path']] += source_dict['next_page']['count_per_page']
            yield scrapy.FormRequest(
                url = source_url,
                method="POST",
                formdata = json.dumps(start_page[source_dict['next_page']['path']]),
                headers = {
                    'content_type' : 'application/x-www-form-urlencoded'
                },
                callback=self.paurse_page,
                meta={'source_url': source_url}
            )
        if source_dict['next_page']['type'] == 'queryString':
            start_page += source_dict['next_page']['count_per_page']
            url_parsed = urlparse(source_url)
            query_string = parse_qs(url_parsed.query)
            query_string[source_dict['next_page']['path']][0] = str(start_page)
            encoded_qs = urlencode(query_string, doseq=1)
            front_url = source_url.split('?')[0]
            next_page_url = f"{front_url}?{encoded_qs}"
            yield scrapy.Request(url=next_page_url, callback=self.paurse_page,meta={'source_url': source_url})


    #parse detail page
    def parse_details(self, response):
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
        # items['_id'] =  uuid.uuid4().hex #มาจากsrc + code
        # items['source'] = 'testBank' #เอามาจาก DB
        # items['url'] = response.url
        # items['img'] = response.css('.modal-map img::attr(src), .items-gallery img::attr(src)').extract()
        # items['gg_map'] = response.css('.btn-col+ .btn-col .button-gray::attr(href)').extract()
        # items['price'] = response.css('.content-price .entry-price::text').extract()
        # items['asset_type'] = response.css('.col-tb:nth-child(1) .info-list p::text').extract()
        # items['asset_code'] = response.css('.col-tb:nth-child(2) p::text').extract()
        # items['area'] = response.css('.col-tb:nth-child(3) p::text').extract()
        # items['deed_num'] = response.css('.col-tb:nth-child(4) p::text').extract()
        # items['address'] = response.css('.col-tb:nth-child(5) p::text').extract()
        # items['contact'] = response.css('.linktel::text').extract()
        # items['more_detail'] = response.css('.col-tb:nth-child(6) p::text').extract()
        yield items

    #when @scr is not absolute url link "../gallery/test.jpg"
    def image_link_check(self,img_array,base_url):
        absolute_url = []
        for img_url in img_array:
            if base_url in img_url:
                absolute_url.append(img_url)
            else:
                if "../" in img_url:
                    img_url =  img_url.replace("../","/")
                absolute__img_url =  f"{base_url}{img_url}"
                absolute_url.append(absolute__img_url)
        return absolute_url
