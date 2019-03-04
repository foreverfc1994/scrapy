# -*- coding: UTF-8 -*-
from urllib import request
import requests
if __name__ == "__main__":
    #访问网址
    url = 'http://blog.163.com/'
    #这是代理IP
    proxy = {'http':'114.230.18.56:4954'}
    #创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    #创建Opener
    opener = request.build_opener(proxy_support)
    #添加User Angent
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    #安装OPener
    request.install_opener(opener)
    #使用自己安装好的Opener
    response = request.urlopen(url)
    #读取相应信息并解码
    html = response.read().decode("utf-8")
    #打印信息
    print(html)
# headers = {
#     'Host':"map.baidu.com",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Connection": "keep-alive",
#     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"
# }
# proxies = {
# 		"http": "http://"+'114.230.18.56:4954',
# 	}
# url = "http://blog.163.com/"
#
# html=requests.get(url,headers=headers,timeout=10,proxies=proxies).text
# print(html)
