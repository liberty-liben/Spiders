# -*- coding: UTF-8 -*-
import scrapy

import string

f = open('//Users/liben/car_price.txt','wb')
line_num = 0
def write_into_file(brand,car_type,price):
    b = brand.encode('utf-8')
    c = car_type.encode('utf-8')
    p = price.encode('utf-8')
    print b,c,p
    f.write(b+'\t'+c+'\t'+p+'\n')

class DmozSpider(scrapy.Spider):
#class DmozSpider(CrawlSpider):
    name = "car_spider"
    allowed_domains = ["car.autohome.com.cn"]
    start_urls = ["http://car.autohome.com.cn/"]

    def parse(self, response):
        #print 'call prase'
        sel = scrapy.Selector(response)

        #按照字母顺序抓取
        for wd in string.uppercase:
            #ids = hxs.select('//*[@id="brand%s"]/span/a/@href'%wd).extract()
            #爬取页面中所有链接品牌报价页面的标签brand_links_tags ,brand_links_tags是一个list
            links = response.xpath('//*[@id="brand%s"]/span/a/@href'%wd).extract()
            for u in links:
                url='http://car.autohome.com.cn'+u
                print url
                yield scrapy.Request(url, callback=self.prase_sub_url)

    def prase_sub_url(self,response):
        #sel = scrapy.Selector(response)
        #获取品牌
        print 'call prase_sub_url'

        brand = response.xpath('/html/body/div[2]/div/div[2]/div[5]/div/div/div[1]/div/a/span/text()').extract()
        print brand[0]

        #获取车型列表下的所有元素
        car_page_list = response.xpath('//div[@class="list-cont-main"]')
        #针对每个车型元素列表，取车型名称和价格
        for index,car_info in enumerate(car_page_list):
            car_type  = car_info.xpath('./div[1]/a/text()').extract()
            price = car_info.xpath('./div[2]/div[2]/div/span/span/text()').extract()
            #print 'line:',index,car_type[0],price[0]
            #将取到的数据存到文件中，数据格式为：品牌；车型；指导价
            yield write_into_file(brand[0],car_type[0],price[0])

        #判断是否有分页，如果有分页，则链接到分页，继续抓取
        next_page = response.xpath('//a[@class="page-item-next"]/@href').extract()
        if len(next_page):
            url='http://car.autohome.com.cn'+next_page[0]
            #print url
            yield scrapy.Request(url,callback=self.prase_sub_url)
