# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#在售二手房源信息
class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()      # 房源信息标题
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
    house_url = scrapy.Field()  # 该房源的url
    zhuangtai = scrapy.Field()  # 房源状态,是否成交
    kanfangshu = scrapy.Field() # 客户看房数
    dengjitime = scrapy.Field() # 房屋登记时间
    zhuaqutime = scrapy.Field()  # 数据抓取时间

#小区信息
class XiaoQuItem(scrapy.Item):
    xiaoqu = scrapy.Field()             #小区名称
    xiaoqu_url = scrapy.Field()         #url
    xiaoqu_longitude = scrapy.Field()   #经度
    xiaoqu_latitude  = scrapy.Field()   #纬度