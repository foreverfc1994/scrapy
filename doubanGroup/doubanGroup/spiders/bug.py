# -*- coding:utf8 -*-
from doubanGroup import settings
import urllib.request
import os
from http import cookiejar
import http.cookiejar
import urllib
from lxml import etree
# proxies = {
#   "http": "http://10.10.1.10:3128",
#   "https": "http://10.10.1.10:1080",
# }
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/javascript, application/javascript,application/ecmascript, application/x-ecmascript, */*; q=0.01',
#     'Accept-Language': 'zh-CN, zh; q=0.8, en-US; q=0.5, en; q=0.3',
#     'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0(Windows NT 10.0; Win64'
#                   '; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
# }
# header=DEFAULT_REQUEST_HEADERS
# def get_num_by_url(url):
#     req = urllib.request.Request(url,headers=header)
#     res = urllib.request.urlopen(req).read().decode()
#     html = etree.HTML(res)
#     list=html.xpath('//*[@id="content"]/div/div[1]/div[2]/ul/li')
#     return len(list)
# def get_rec_num(url):
#     rec_num = 0
#     i=1
#     rec_url=url+'?type=rec#sep'
#     req = urllib.request.Request(rec_url,headers=header)
#     res = urllib.request.urlopen(req).read().decode()
#     html = etree.HTML(res)
#     is_page=html.xpath('//*[@id="content"]/div/div[1]/div[4]')
#     num = len(html.xpath('//*[@id="content"]/div/div[1]/div[3]/ul/li'))
#     rec_num += num
#     if is_page:
#         page_num=html.xpath('//*[@id="content"]/div/div[1]/div[4]/a/text()')[-1]
#         while i<int(page_num):
#             page_url=url+'?type=like&start='+str(i*100)+'#sep'
#             this_page_num=get_num_by_url(page_url)
#             rec_num+=this_page_num
#             i+=1
#     else:
#         pass
#
# def get_like_num(url):
#     like_num = 0
#     i=1
#     like_url=url+'?type=like#sep'
#     req = urllib.request.Request(like_url,headers=header)
#     res = urllib.request.urlopen(req).read().decode()
#     print(res)
#     html = etree.HTML(res)
#     is_page=html.xpath('//*[@id="content"]/div/div[1]/div[4]')
#     num = len(html.xpath('//*[@id="content"]/div/div[1]/div[3]/ul/li'))
#     like_num += num
#     if is_page:
#         page_num=html.xpath('//*[@id="content"]/div/div[1]/div[4]/a/text()')[-1]
#         while i<int(page_num):
#             page_url=url+'?type=rec&start='+str(i*100)+'#sep'
#             this_page_num=get_num_by_url(page_url)
#             like_num+=this_page_num
#             i+=1
#     else:
#         pass
# url='https://www.douban.com/group/topic/110586820/'
# get_like_num(url)
# get_rec_num(url)
# def get_fans(url):
#     req = urllib.request.Request(url, headers=header)
#     res = urllib.request.urlopen(req).read().decode()
#     html=etree.HTML(res)
#     is_page=html.xpath('//*[@id="content"]/div/div[1]/div[3]')
#     fans_list=html.xpath('//*[@id="content"]/div/div[1]/dl[@class="obu"]')
#     for i in fans_list:
#         fan_pic=i.xpath('./dt/a/img/@src')
#         print(type(fan_pic))
#
# from doubanGroup.utils.login_api import login,get_captcha,get_login_cookie
# #rl = 'https://www.douban.com/people/1835526/contacts'
# url='https://www.douban.com/people/1835526/rev_contacts'
# header=settings.DEFAULT_REQUEST_HEADERS_1
# cookie_file=settings.COOKIE_FILE
# user_name = '741733238@qq.com'
# password = 'fc741733238fc'
# login(user_name,password,cookie_file)
# get_fans(url)
# req=urllib.request.Request(url,headers=header)
# res=urllib.request.urlopen(req).read().decode()
# print(res)
# print('-------------------------------------------------------------------------------------')
# req2=urllib.request.Request(url2,headers=header)
# res2=urllib.request.urlopen(req2).read().decode()
# print(res2)



