#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import scrapy
import time
from scrapy.spiders import Spider
from scrapy.selector import Selector
from lianjia.items import LianjiaItem
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tag_dict = {
    "taxfree-ex":"tag_man",
    "fang-subway-ex":"tag_ditie",
    "fang05-ex":"tag_xuequ",
    "is_restriction-ex":"tag_xg"
}
class LianjiaSider(Spider):
    name = 'lianjia_spider'
    allowed_domains = ['bj.lianjia.com']
    download_delay = 1
    count = 0
    start_urls = [
        "http://bj.lianjia.com/ershoufang/", #二手房
        #"http://bj.lianjia.com/ditiefang/",  #地铁房
        #"http://bj.lianjia.com/xuequfang/",  #学区房
        #"http://bj.lianjia.com/chengjiao/"   #成交房源
    ]
    #抓取二手房网页的房源列表
    def parse(self, response):
        sel = Selector(response)
        #获取房屋信息列表houst_list
        house_list = sel.xpath('//ul[@id="house-lst"]/li')

        #获取房源列表中的房源url
        for house in house_list:
            self.count+=1
            #house_id = house.xpath('.//@data-id').extract().encode('utf-8')
            house_url = house.xpath('.//div[@class="pic-panel"]/a/@href').extract()[0]
            yield scrapy.Request(house_url, callback=self.sell_house_parse)
            print self.count
            #print house_url
            if self.count > 1:
                break

        #获取下一页的信息
        #获取page-box节点,并拼装下一页的url
        page_box = sel.xpath('//div[@class="page-box house-lst-page-box"]')
        pageurl=page_box.xpath('.//@page-url').extract()[0].encode('utf-8')
        pagedata=page_box.xpath('.//@page-data').extract()[0].encode('utf-8')
        #print pagedata
        #当前页
        curpage = eval(pagedata)["curPage"]
        #总页数
        totalpage = eval(pagedata)['totalPage']
        #顺序读取下一页
        if totalpage > curpage:
            p = re.compile(r'^/\w*/\w*')
            nexturl=p.findall(pageurl)[0]
            next_page_url='http://bj.lianjia.com'+nexturl+str(curpage+1)
            #print next_page_url
            time.sleep(0.5)
            yield scrapy.Request(next_page_url, callback=self.parse)

    #解析房源信息
    def sell_house_parse(self,response):
        #创建LianjiaItem对象
        item = LianjiaItem()
        sel = Selector(response)
        #标题行信息
        title_line = sel.xpath('//div[@class="title-line clear"]')
        #获取房产的标题
        item['title'] = title_line.xpath('.//h1[@class="title-box left"]/text()').extract()[0]

        #根据第一条评论信息,获取房源的登记信息,
        #//*[@id="commentsCon"]/div[1]/div[1]/p[1]/text()
        pinglun = sel.xpath('//*[@id="firstData"]/text()').extract()[0]
        # 解析成中文
        pl_str = json.loads(json.dumps(pinglun).replace("\\\\","\\"))
        #获取第一条评论的时间作为房源登记时间
        reg = re.compile(r'\"lastModifyTime\"\:\"[0-9\-\:\ ]*\"')
        doc=reg.findall(pl_str)
        #print 'dengji',doc[0][18:29]
        #print pl_str
        #print dict(doc)['lastModifyTime']
        item['dengjitime'] = doc[0][18:29]

        #房产的标签信息
        view_labels = sel.xpath('.//div[@class="view-label"]/span')
        #print len(view_labels)
        for label in view_labels:
            label_class = label.xpath('.//@class').extract()[0]
            #print "label",label_class
            if label_class in tag_dict.keys():
                item[tag_dict[label_class]] = label.xpath('.//span/text()').extract()[0]

        #房屋详细信息
        house_info = sel.xpath('//div[@class="info-box left"]')
        #获取售价
        jiaqian = house_info.xpath('.//span[@class="em-text"]/strong/text()').extract()[0]
        danwei = house_info.xpath('.//span[@class="em-text"]/span/text()').extract()[0]
        item['shoujia'] =jiaqian+danwei
        #获取面积
        mianji = house_info.xpath('.//span[@class="em-text"]/i/text()').extract()[0]
        item['mianji'] = mianji.split('/')[-1].strip()
        #获取单价
        item['danjia']=house_info.xpath('.//dl[2]/dd/text()').extract()[0]
        #获取首付
        item['shoufu']=house_info.xpath('.//dl[3]/dd/text()').extract()[0]
        #获取月供
        item['yuegong']=house_info.xpath('.//dl[4]/dd/text()').extract()[0]
        #获取户型
        item['huxing']=house_info.xpath('.//dl[5]/dd/text()').extract()[0]
        #获取朝向
        chaoxiang=house_info.xpath('.//dl[6]/dd/text()').extract()[0]
        #item['chaoxiang'] = chaoxiang.split()
        cx_list = chaoxiang.split()
        item['chaoxiang'] = cx_list
        #获取楼层
        item['louceng']=house_info.xpath('.//dl[7]/dd/text()').extract()[0]
        #获取小区
        item['yuegong']=house_info.xpath('.//dl[8]/dd/a/text()').extract()[0]
        #获取城区
        item['chengqu']=house_info.xpath('.//dl[8]/dd/span/a[1]/text()').extract()[0]
        #获取商圈
        item['shangquan']=house_info.xpath('.//dl[8]/dd/span/a[2]/text()').extract()[0]
        #获取年份
        item['nianfen']=house_info.xpath('.//dl[8]/dd/text()').extract()[0]
        #获取客户看房数
        item['kanfangshu']=sel.xpath('//div[@class="house-del"]/ul/li[3]/div/span[2]/text()').extract()[0]
        #获取房源编号:
        item['house_id']=sel.xpath('//div[@class="iinfo right"]/p[1]/span[2]/text()').extract()[0]
        #设置房源状态:在售:1,成交:0
        item['zhuangtai'] = 1
        #设置抓取时间
        item['zhuaqutime'] = time.strftime( '%Y-%m-%d', time.localtime() )
        yield item

        #print(title,tag_man,tag_ditie,tag_xuequ,tag_xg)