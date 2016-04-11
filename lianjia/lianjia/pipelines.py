# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pymongo import MongoClient


def get_db():
    client = MongoClient( DB_ADDRESS, DB_PORT )
    db = client[DB_NAME]
    db.authenticate( DB_USER, DB_PASS )
    return db


class LianjiaPipeline(object):

    def __init__(self):
        self.file = open('/Users/liben/PycharmProjects/Spiders/lianjia/lianjia_item.json','wb')
        self.db_address = 'localhost'
        self.db_port = 27017
        self.db_name = 'lianjia'
        self.collection_name = 'house'

    @classmethod
    def from_crawler(cls,crawler):
        return (

        )
    def process_item(self, item, spider):
        line = json.dumps(dict(item))+'\n'
        #因为抓取的数据是unicode编码,所以要进行解码decode('unicode_escape')
        self.file.write(line.decode('unicode_escape'))
        return item
