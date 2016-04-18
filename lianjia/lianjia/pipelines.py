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


class LianjiaPipeline(object):

    def __init__(self):
#        self.file = open('/Users/liben/PycharmProjects/Spiders/lianjia/lianjia_item.json','wb')
        self.db_address = 'localhost'
        self.db_port = 27017
        self.db_name = 'lianjia'
        self.collection_name = 'house'

    def open_spider(self,spider):
        self.clent = MongoClient(self.db_address,self.db_port)
        self.db = self.clent[self.db_name]

    def close_spider(self,spider):
        self.clent.close()

    def process_item(self, item, spider):
        data = dict(item)
        #line = json.dumps(data)+'\n'
        #因为抓取的数据是unicode编码,所以要进行解码decode('unicode_escape')
        #self.file.write(line.decode('unicode_escape'))
        #self.db[self.collection_name].insert(data)
        self.db[self.collection_name].update({'_id':data['house_id']},{'$set':data},True)

        return item
