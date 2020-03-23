# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags

def remove_html(text_data):
    cleaned_data = ''
    try:
        cleaned_data = remove_tags(text_data)
    except TypeError:
        cleaned_data = 'No data'
    return cleaned_data

def remove_space_tag(text_data):
    if "\n" in text_data:
        text_data.replace('\n','')
    if "&nbsp" in text_data:
        text_data.replace('&nbsp','')
    return text_data


class NpaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    _id = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    gg_map = scrapy.Field()
    price = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    asset_type = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    asset_code = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    area = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    deed_num = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    address = scrapy.Field(
        input_processor = MapCompose(remove_html,remove_space_tag)
    )
    contact = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    more_detail = scrapy.Field(
        input_processor = MapCompose(remove_html, remove_space_tag)
    )
    # pass
