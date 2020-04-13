# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags



class NpaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    _id = scrapy.Field()
    source = scrapy.Field()
    asset_url = scrapy.Field()
    asset_img = scrapy.Field()
    gg_map = scrapy.Field()
    price = scrapy.Field()
    asset_type = scrapy.Field()
    asset_code = scrapy.Field()
    area = scrapy.Field()
    area_rai = scrapy.Field()
    area_ngan = scrapy.Field()
    area_sq_wa = scrapy.Field()
    deed_num = scrapy.Field()
    address = scrapy.Field()
    province = scrapy.Field()
    district = scrapy.Field()
    sub_district = scrapy.Field()
    contact = scrapy.Field()
    more_detail = scrapy.Field()
    update_date = scrapy.Field()
    status = scrapy.Field()
    # pass
