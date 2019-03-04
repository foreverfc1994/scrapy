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
    class_ = scrapy.Field()
    publish_time = scrapy.Field()
    #来源
    resource = scrapy.Field()
    #分类
    category = scrapy.Field()
    content = scrapy.Field()
    picture_href = scrapy.Field()
    picture_path = scrapy.Field()
    #责任编辑
    tags = scrapy.Field()
    editor = scrapy.Field()
    md5 = scrapy.Field()
    targetid = scrapy.Field()
    comment_num = scrapy.Field()
    comment_ids = scrapy.Field()
class commentItem(scrapy.Item):
    targetid = scrapy.Field()
    created_time = scrapy.Field()
    userid = scrapy.Field()
    up = scrapy.Field()
    replynum = scrapy.Field()
    id = scrapy.Field()
    #indexscore = scrapy.Field()
    content = scrapy.Field()
class replyItem(scrapy.Item):
    targetid = scrapy.Field()
    parent = scrapy.Field()
    userid = scrapy.Field()
    created_time = scrapy.Field()
    content = scrapy.Field()
    up = scrapy.Field()
    id =scrapy.Field()