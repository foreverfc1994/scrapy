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
    comment_count = scrapy.Field()
    comment_ids = scrapy.Field()
    tags = scrapy.Field()
    md5 = scrapy.Field()

class commentItem(scrapy.Item):
    author_name = scrapy.Field()
    created_time = scrapy.Field()
    author_id  =scrapy.Field()
    news_id = scrapy.Field()
    content = scrapy.Field()
    zan_count = scrapy.Field()