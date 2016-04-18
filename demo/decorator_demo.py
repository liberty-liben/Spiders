# class Student(object):
#     def __init__(self, name, score):
#         self.name = name
#         self.__score = score
#     @property
#     def score(self):
#         return self.__score
#     @score.setter
#     def score(self, score):
#         if score < 0 or score > 100:
#             raise ValueError('invalid score')
#         self.__score = score
#     @property
#     def grade(self):
#         if self.score < 60:
#             return 'C'
#         if self.score < 80:
#             return 'B'
#         return 'A'
# s = Student('Bob', 59)
# print s.grade
# s.score = 60
# print s.grade
# s.score = 99
# print s.grade

# import re
#
# p = re.compile(r'^/\w*/\w*')
# str = '/ershoufang/pg{page}/'
# print p.findall(str)[0]

#/usr/local env python
#coding utf-8
import os
import urllib
from bs4 import BeautifulSoup
ip = ''
def log():
    f=open("/Users/liben/PycharmProjects/Spiders/demo/daili.txt",'a')
    f.write(ip)
    f.close()

def fenxi():
    page = urllib.urlopen(url)
    data = page.read()
    soup=BeautifulSoup(data)
    #print soup
    list=soup.find_all('span')
    for i in list:
        #print i.get_text()
        #global ip
        ip= i.get_text()
        s="\n".join(ip.split('#'))
        print s
for i in range(1,10):
    log()
    if i==1:
        url = 'http://www.youdaili.net/Daili/http/4342.html'
        print url
        fenxi()
    else:
        url = 'http://www.youdaili.net/Daili/http/556_'+str(i)+'.html'
        print url
        fenxi()
