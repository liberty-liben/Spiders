#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup



url = 'http://baike.baidu.com/view/21087.htm'
response1 = urllib2.urlopen(url)
html_doc = response1.read()

soup = BeautifulSoup(
    html_doc,
    'html.parser',
    from_encoding='utf-8'
)

print('获取所有的连接')
links = soup.find_all('a',target='_blank')

for link in links:
    print link.name,link['href'],link.get_text()

