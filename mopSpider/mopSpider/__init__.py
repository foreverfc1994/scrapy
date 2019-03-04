# # import time
# # import datetime
# # format = '%Y-%m-%d %H:%M:%S'
# # d=datetime.datetime.now()
# # t=datetime.datetime.timestamp(d)
# import re
# str='{\"imgheight\":\"160\",\"imgmd5\":\"b4dbb6a684227d37013c11022d823ab5\",\"imgname\":\"20171224_51590c844452f00e914a4f2ac166aeb9_15_8_300.jpg\",\"imgwidth\":\"300\",\"src\":\"http://images01.mopimg.cn/imgs/20171224/20171224_51590c844452f00e914a4f2ac166aeb9_15_8_300.jpg\"}]","replynum":119,"readnum":41420,"praisenum":3,"recommendnum":1,"favoritenum":1,"rdts":858977,"htmlname":"171224124822288858977.html","url":"http://dzh.mop.com/a/171224124822288858977.html","cts":1514090902288,"videojs":null,"videoajs":null,"videobjs":null,"videoalltime":null,"videoplaytimes":null,"psource":null,"jsonurl":"http://dc.mop.com/subject/a/171224124822288858977.json","headurl":null,"resources":null,"sex":null,"level":null,"levelDesc":null,"numMap":null}})'
# a=re.compile(r'"replynum":\w+,')
# b=re.compile(r'"readnum":\w+,')
# c=re.compile(r'"praisenum":\w+,')
# d=re.compile(r'"recommendnum":\w+,')
# e=re.compile(r'"favoritenum":\w+,')
# replynum=re.search(a,str).group().split(':')[-1].split(',')[0]
# readnum=re.search(b,str).group().split(':')[-1].split(',')[0]
# praisenum=re.search(c,str).group().split(':')[-1].split(',')[0]
# recommendnum=re.search(d,str).group().split(':')[-1].split(',')[0]
# favoritenum=re.search(e,str).group().split(':')[-1].split(',')[0]
#
# print(replynum,readnum,praisenum,recommendnum,favoritenum)