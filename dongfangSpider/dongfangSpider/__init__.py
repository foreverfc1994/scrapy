# import urllib.request
# import re
# import json
# from bs4 import BeautifulSoup
# url = 'http://mini.eastday.com/a/180130233350447-2.html'
# req = urllib.request.Request(url)
# res = urllib.request.urlopen(req).read().decode()
# print(res)
# print('-----------------------------------------------')
#
# # res = eval(res)
# # print(res)
# # dict_keys(['rev', 'rowkey', 'idx', 'issyncart', 'isreport', 'userid', 'at', 'isRoboot',
# #            'aid', 'isban', 'date', 'userpic', 'news_type', 'apptypeid', 'isblack', 'content',
# #            'ding', 'username', 'reviewto', 'isaudit', 'ck', 'auditflag', 'quality', 'cts'])
#
# # json_data = json.loads(res)
# # a= json_data['data']
# # for i in a:
# #     print(i)
# # soup = BeautifulSoup(res,"html.parser")
# # a=soup.find_all('div',class_='pagination')[0]
# # print(a)
# # b=a.find_all('a')[-2].string
# # print(b)
