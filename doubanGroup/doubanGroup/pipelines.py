# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from hbase import THBaseService
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
#from thrift.protocol import TCompactProtocol
#from thrift.transport import TSocket

# from doubanGroup.items import PostItem, AuthorItem, CommentItem, GroupItem, FansItem
# from doubanGroup.utils.gen_db_put import gen_start_spider_info, gen_stop_spider_info, gen_author_put, gen_post_put, \
#     gen_comment_put, gen_group_put, gen_fans_put, TTransport


# class ImagePipeline(ImagesPipeline):
#     @classmethod
#     def from_settings(cls, settings):
#         global store_uri
#         store_uri = settings['IMAGES_STORE']
#         return cls(store_uri, settings=settings)
#
#     def get_media_requests(self, item, info):
#         if isinstance(item, PostItem) and 'picture_hrefs' in item and item['picture_hrefs']:
#             for picture_url in item['picture_hrefs']:
#                 yield Request(picture_url)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#
#         local_uri = [store_uri + image_path for image_path in image_paths]
#
#         if isinstance(item, PostItem):
#             item['picture_path'] = local_uri
#
#         return item
#
#
# class SaveHBasePipeline(object):
#     def __init__(self, settings):
#         self.DB_URI = settings['HBASE_URI']
#         self.DB_PORT = settings['HBASE_PORT']
#         self.TB_INFO = settings['TB_INFO'].encode()
#         self.TB_POST = settings['TB_POST'].encode()
#         self.TB_AUTHOR = settings['TB_AUTHOR'].encode()
#         self.TB_COMMENT = settings['TB_COMMENT'].encode()
#         self.TB_FANS = settings['TB_FANS'].encode()
#         self.TB_GROUP = settings['TB_GROUP'].encode()
#
#         # 连接数据库表
#         socket = TSocket.TSocket(self.DB_URI, self.DB_PORT)
#         self.transport = TTransport.TFramedTransport(socket)
#         protocol = TCompactProtocol.TCompactProtocol(self.transport)
#         self.client = THBaseService.Client(protocol)
#
#         self.transport.open()
#         # 将爬虫开始的信息存入数据库
#         self.spider_info_row_key, start_put = gen_start_spider_info()
#         self.client.put(self.TB_INFO, start_put)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.spider.settings
#         return cls(settings=settings)
#
#     def close_spider(self, spider):
#         # 存储爬虫结束的信息
#         stop_put = gen_stop_spider_info(self.spider_info_row_key)
#         # noinspection PyBroadException
#         try:
#             self.client.put(self.TB_INFO, stop_put)
#         except Exception:
#             print('close spider put failure!')
#             self.transport.close()
#             self.transport.open()
#             self.client.put(self.TB_INFO, stop_put)
#         self.transport.close()
#
#     def process_item(self, item, spider):
#         table = None
#         item_put = None
#         if isinstance(item, AuthorItem):
#             _, item_put = gen_author_put(item)
#             table = self.TB_AUTHOR
#         elif isinstance(item, PostItem):
#             _, item_put = gen_post_put(item)
#             table = self.TB_POST
#         elif isinstance(item, CommentItem):
#             _, item_put = gen_comment_put(item)
#             table = self.TB_COMMENT
#         elif isinstance(item, GroupItem):
#             _, item_put = gen_group_put(item)
#             table = self.TB_GROUP
#         elif isinstance(item, FansItem):
#             _, item_put = gen_fans_put(item)
#             table = self.TB_FANS
#
#         # noinspection PyBroadException
#         if table:
#             # noinspection PyBroadException
#             try:
#                 self.client.put(table, item_put)
#             except Exception:
#                 print('news item put failure!')
#                 self.transport.close()
#                 self.transport.open()
#                 self.client.put(table, item_put)
#
#         return item
# class SaveTestPipeline(object):
#     def process_item(self, item, spider):
#         print(item)
from doubanGroup import settings
# from doubanGroup.items import GroupItem
# import pymysql
# def dbHandle():
#     conn = pymysql.connect(
#         host='localhost',
#         user='root',
#         passwd='foreverfc',
#     )
#     return conn
# class DoubanMysqlPipeline(object):
#
#     def process_item(self, item, spider):
#         dbObject=dbHandle()
#         cursor=dbObject.cursor()
#         print(1)
#         if isinstance(item, GroupItem):
#             # sql='insert into douban_group.groupitem(url,group_id,group_name,create_time,leader_name,leader_href,content,group_tags)'
#             # #try:
#             # cursor.execute(sql,(item['url'].encode(),item['group_id'].encode(),item['group_name'].encode(),item['create_time'].encode(),item['leader_name'].encode(),item['leader_href'].encode(),item['content'].encode(),item['group_tags'].encode()))
#             sql='insert into douban_group.groupitem(url)'
#             cursor.execute(sql,(str(item['url'].encode())))
#             dbObject.commit()
#             print("insert succeed")
#             # except Exception as e:
#             #     print(e)
#         else:
#             print("it is not a group")
#
import pymysql
from doubanGroup.items import GroupItem,AuthorItem,CommentItem,FansItem,PostItem

class DoubanMysqlPipeline(object):
    #def __init__(self, mysql_uri, mysql_user_name, mysql_password, mysql_db):
    def __init__(self):
        self.mysql_uri = 'localhost'
        self.mysql_user_name = 'root'
        self.mysql_password = 'foreverfc'
        self.mysql_db = 'douban_group'

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mysql_uri=crawler.settings.get('MYSQL_URI'),
    #         mysql_user_name=crawler.settings.get('MYSQL_USER_NAME'),
    #         mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
    #         mysql_db=crawler.settings.get('MYSQL_DB')
    #     )

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            self.mysql_uri,
            self.mysql_user_name,
            self.mysql_password,
            self.mysql_db,
            charset='utf8'
        )

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        cursor = self.connect.cursor()

        sql = self.generate_insert_sql(item)
        if sql:
            try:
               cursor.execute(sql)
               self.connect.commit()
            except Exception as e:
                print(e)

        cursor.close()
        return item

    def generate_insert_sql(self, item):
        if isinstance(item,GroupItem):
            tb_name = 'groupitem'
        elif isinstance(item,PostItem):
            tb_name = 'postitem'
        elif isinstance(item,AuthorItem):
            tb_name = 'authoritem'
        elif isinstance(item,FansItem):
            tb_name = 'fansitem'
        elif isinstance(item,CommentItem):
            tb_name = 'commentitem'
        # if tb_name=='commentitem':
        #     print(item)
        #     input("lalalal")

        sql = 'INSERT INTO ' + tb_name + ' ('
        tb_fields = ''
        tb_values = ''
        for tb_f in item:
            tb_fields = tb_fields + tb_f + ', '
            tb_values = tb_values + '"' + str(item[tb_f]) + '", '

        return sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'
#if __name__ == '__main__':