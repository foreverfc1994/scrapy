# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class newsItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    #来源
    resource = scrapy.Field()
    #分类
    category = scrapy.Field()
    content = scrapy.Field()
    picture_href = scrapy.Field()
    picture_path = scrapy.Field()
    #责任编辑
    editor = scrapy.Field()
    md5 = scrapy.Field()