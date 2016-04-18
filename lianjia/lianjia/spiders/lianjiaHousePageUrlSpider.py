#!/usr/bin/env python
# -*- coding:utf-8 -*-

#数据抓取的逻辑:
        # 1)先抓取各个区域的url
        # 2)在区域的页面中,抓取商圈的urls
        # 3)在商圈的页面抓抓取房源列表的urls
        # 4)抓取每个房源信息.

import re
import scrapy

from scrapy.spiders import Spider
from scrapy.selector import Selector

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url_pre = 'http://bj.lianjia.com'

class LianjiaSider(Spider):
    name = 'lianjiaHousePageUrlSpider'
    allowed_domains = ['bj.lianjia.com']
    count = 0
    start_urls = [
        "http://bj.lianjia.com/ershoufang/", #二手房
        #"http://bj.lianjia.com/ditiefang/",  #地铁房
        #"http://bj.lianjia.com/xuequfang/",  #学区房
        #"http://bj.lianjia.com/chengjiao/"   #成交房源
    ]

    #进入二手房页面,抓取,抓取区域url
    def parse(self, response):
        # print response.meta
        # print time.time()
        sel = Selector(response)
        #获取北京各个区域的url列表:
        area_urls = {}

        area_url_list = sel.xpath('//*[@id="filter-options"]/dl[1]/dd/div[1]/a[@href]')
        for arl in area_url_list:
            area = arl.xpath('./text()').extract()[0].encode('utf-8')
            url = arl.xpath('./@href').extract()[0].encode('utf-8')
            area_urls[area]=url_pre+url
        count =1
        for k in area_urls.keys():
            url = area_urls.get(k)
            #针对每个区域,开始抓取各个子商圈的url
            yield scrapy.Request(url,callback=self.parse_business_area)

    #抓取商圈url
    def parse_business_area(self,response):
        # print response.meta
        # print time.time()
        sel = Selector(response)
        #获取北京各个区域的url列表:
        business_area_urls = {}
        starurl = 'http://bj.lianjia.com'
        area_url_list = sel.xpath('//*[@id="filter-options"]/dl[1]/dd/div[2]/a[@href]')
        for arl in area_url_list:
            area = arl.xpath('./text()').extract()[0].encode('utf-8')
            url = arl.xpath('./@href').extract()[0].encode('utf-8')
            business_area_urls[area]=starurl+url

        for k in business_area_urls:
            url = business_area_urls.get(k)
            #print k,url
            yield scrapy.Request(url,callback=self.parse_house_page_list)

    #抓取每个商圈中的房源列表页
    def parse_house_page_list(self,response):
        # print response.meta
        sel = Selector(response)
        house_page_list = []
        title = sel.xpath('/html/body/div[6]/div[2]/div[1]/h3/span[1]/a/text()').extract()[0].encode('utf-8')
        #获取page-box节点,并拼装下一页的url
        page_box = sel.xpath('//div[@class="page-box house-lst-page-box"]')
        box = page_box.extract()
        if len(box)>0:
            pageurl=page_box.xpath('.//@page-url').extract()[0].encode('utf-8')
            pagedata=page_box.xpath('.//@page-data').extract()[0].encode('utf-8')
            #print pagedata
            p = re.compile(r'^[/\w]*')
            page_url=p.findall(pageurl)[0]
            #print pageurl,page_url
            #总页数
            totalpagenum = eval(pagedata)['totalPage']
            #print title,totalpagenum
            for i in range(1,totalpagenum+1):
                house_page_url = 'http://bj.lianjia.com'+page_url+str(i)
                house_page_list.append(house_page_url)
                #print house_page_url
            for i in house_page_list:
                #print i
                yield scrapy.Request(i, callback=self.parse_house)

    def parse_house(self,response):
        sel = Selector(response)
        #获取房屋信息列表houst_list
        house_list = sel.xpath('//ul[@id="house-lst"]/li')
        #获取房源列表中的房源url
        for house in house_list:
            #self.count+=1
            #house_id = house.xpath('.//@data-id').extract().encode('utf-8')
            house_url = house.xpath('.//div[@class="info-panel"]/a/@href').extract()
            if len(house_url)>0:
                yield scrapy.Request(house_url[0], callback=self.parse_house_info)
            #print self.count,house_url
            #print house_url
            #if self.count > 1:
                #break
