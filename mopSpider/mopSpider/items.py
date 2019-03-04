# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    url = scrapy.Field()

    post_id = scrapy.Field()
    #？？？？？？
    path_text = scrapy.Field()
    path_href = scrapy.Field()

    title = scrapy.Field()
    #发表时间
    publish_date = scrapy.Field()
    #浏览次数
    hits = scrapy.Field()
    #评论数量
    reply_num = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    tags = scrapy.Field()
    #赞，推荐，收藏
    praise_num = scrapy.Field()
    recommend_num = scrapy.Field()
    collect_num = scrapy.Field()

    comment_ids = scrapy.Field()


class AuthorItem(scrapy.Item):
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    sex = scrapy.Field()
    location = scrapy.Field()
    age = scrapy.Field()
    level = scrapy.Field()
    level_nick = scrapy.Field()

    friends_num = scrapy.Field()
    fans_num = scrapy.Field()
    # 积分
    point = scrapy.Field()
    #发帖数量
    post_num = scrapy.Field()
    #回帖数量
    reply_num = scrapy.Field()
    #访问量
    hits = scrapy.Field()

    birthday = scrapy.Field()
    #上次登录时间
    login_num = scrapy.Field()
    introduce = scrapy.Field()

    register_date = scrapy.Field()
    #联盟
    league = scrapy.Field()
    #联系方式
    contact_way = scrapy.Field()
    #教育背景
    education = scrapy.Field()
    #职业信息
    career = scrapy.Field()


class CommentItem(scrapy.Item):
    post_id = scrapy.Field()

    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    user_href = scrapy.Field()
    user_name = scrapy.Field()

    date_time = scrapy.Field()
    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()
    #赞，回复，几楼
    praise_num = scrapy.Field()
    reply_num = scrapy.Field()

    floor_num = scrapy.Field()


class FansItem(scrapy.Item):
    fans_id = scrapy.Field()
    friends_id = scrapy.Field()

