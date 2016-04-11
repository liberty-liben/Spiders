#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import scrapy
import time
from scrapy.spiders import Spider
from scrapy.selector import Selector


class LianjiaSider(Spider):
    name = 'lianjia_spider'
    allowed_domains = ['bj.lianjia.com']
    start_urls = [
        "http://bj.lianjia.com/ershoufang/", #二手房
        #"http://bj.lianjia.com/ditiefang/",  #地铁房
        #"http://bj.lianjia.com/xuequfang/",  #学区房
        #"http://bj.lianjia.com/chengjiao/"   #成交房源
    ]

    def parse(self, response):
        sel = Selector(response)
        #获取房屋信息列表houst_list
        house_list = sel.xpath('//ul[@id="house-lst"]')

        #获取下一页的信息
        #获取page-box节点,并拼装下一页的url
        page_box = sel.xpath('//div[@class="page-box house-lst-page-box"]')
        pageurl=page_box.xpath('.//@page-url').extract()[0].encode('utf-8')
        pagedata=page_box.xpath('.//@page-data').extract()[0].encode('utf-8')
        print pagedata

        curpage = eval(pagedata)["curPage"]
        totalpage = eval(pagedata)['totalPage']
        if totalpage > curpage:
            p = re.compile(r'^/\w*/\w*')
            nexturl=p.findall(pageurl)[0]
            next_page_url='http://bj.lianjia.com'+nexturl+str(curpage+1)
            print next_page_url
            time.sleep(0.05)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # def prase_sub_url(self,response):
    #     pass
    #
