# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from hbase import THBaseService
from scrapy import Request
import pymysql
from scrapy.pipelines.images import ImagesPipeline
# from thrift.protocol import TCompactProtocol
# from thrift.transport import TSocket
#
from tianyaBBSSpider.items import PostItem, CommentItem, AuthorItem, FansItem

#
#
class ImagePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if isinstance(item, PostItem) and 'picture_href' in item and item['picture_href']:
            for picture_url in item['picture_href']:
                yield Request(picture_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        local_uri = [store_uri + image_path for image_path in image_paths]

        if isinstance(item, PostItem):
            item['picture_path'] = local_uri

        return item
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
#         elif isinstance(item, FansItem):
#             _, item_put = gen_fans_put(item)
#             table = self.TB_FANS
#         # noinspection PyBroadException
#         if table:
#             try:
#                 self.client.put(table, item_put)
#             except Exception:
#                 print('news item put failure!')
#                 self.transport.close()
#                 self.transport.open()
#                 self.client.put(table, item_put)
#
#         return item
class TianyaMysqlPipeline(object):
    def __init__(self):
        self.mysql_uri = 'localhost'
        self.mysql_user_name = 'root'
        self.mysql_password = 'foreverfc'
        self.mysql_db = 'tianyabbs'

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
        if isinstance(item,PostItem):
            tb_name = 'post'
        elif isinstance(item,AuthorItem):
            tb_name = 'author'
        elif isinstance(item,FansItem):
            tb_name = 'fans'
        elif isinstance(item,CommentItem):
            tb_name = 'comment'

        sql = 'INSERT INTO ' + tb_name + ' ('
        tb_fields = ''
        tb_values = ''
        for tb_f in item:
            tb_fields = tb_fields + tb_f + ', '
            tb_values = tb_values + '"' + str(item[tb_f]) + '", '

        return sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'
