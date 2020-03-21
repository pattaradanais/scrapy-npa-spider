# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NpaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    _id = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    gg_map = scrapy.Field()
    price = scrapy.Field()
    asset_type = scrapy.Field()
    asset_code = scrapy.Field()
    area = scrapy.Field()
    deed_num = scrapy.Field()
    address = scrapy.Field()
    contact = scrapy.Field()
    more_detail = scrapy.Field()
    # pass
