# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    house_id = scrapy.Field()   # 房源编号
    shoujia = scrapy.Field()    # 售价
    mianji = scrapy.Field()     # 房屋面积
    danjia = scrapy.Field()     # 单价
    shoufu  = scrapy.Field()    # 首付
    yuegong = scrapy.Field()    # 月供
    huxing = scrapy.Field()     # 户型
    chaoxiang = scrapy.Field()  # 朝向
    louceng = scrapy.Field()    # 楼层
    xiaoqu = scrapy.Field()     # 小区
    chengqu = scrapy.Field()    # 城区
    shangquan = scrapy.Field()  # 商圈
    nianfen = scrapy.Field()    # 建筑年份
    tag_man = scrapy.Field()    # 满五唯一\满2
    tag_ditie = scrapy.Field()  # 近地铁
    tag_xuequ = scrapy.Field()  # 学区房
    tag_xg = scrapy.Field()     # 不限购