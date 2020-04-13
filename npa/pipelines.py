# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class NpaPipeline(object):
    def __init__(self):
        # client = pymongo.MongoClient("mongodb+srv://npaDB:npaadmin@cluster0-ipibu.gcp.mongodb.net/npaWebAppDB?retryWrites=true&w=majority")
        client = pymongo.MongoClient("mongodb://npaDB:npaadmin@cluster0-shard-00-00-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-01-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-02-ipibu.gcp.mongodb.net:27017/npaWebAppDB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        db = client.get_default_database()
        self.collection = db['properties']
        # pass

    def process_item(self, item, spider):
        self.collection.update({'_id':item['_id']},dict(item),upsert=True)
        return item
