# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BQMysqlPipeline(object):
    def __init__(self):
        self.mysql_uri = 'localhost'
        self.mysql_user_name = 'root'
        self.mysql_password = 'foreverfc'
        self.mysql_db = 'beiqing'

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
        tb_name = 'news'

        sql = 'INSERT INTO ' + tb_name + ' ('
        tb_fields = ''
        tb_values = ''
        for tb_f in item:
            tb_fields = tb_fields + tb_f + ', '
            tb_values = tb_values + '"' + str(item[tb_f]) + '", '

        return sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'