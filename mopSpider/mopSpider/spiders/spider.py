#! /usr/bin python3
# -*- coding: utf-8 -*-
import json
from lxml import etree
import urllib
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
import re
from scrapy_redis.spiders import RedisCrawlSpider
from mopSpider.items import FansItem
from mopSpider.spiders.author import get_author_item
from mopSpider.spiders.comment import unix_to_time,time_to_unix
from mopSpider.items import CommentItem
from mopSpider.spiders.fans import get_fans_item
from mopSpider.spiders.post import get_post_item,get_comment_data


class MopSpider(CrawlSpider):
    name = 'mop'

    allowed_domains = ['mop.com']
    #redis_key = "mopspider:start_urls"
    start_urls = ['http://dzh.mop.com/']
    #start_urls = ['http://dzh.mop.com/a/171224124822288858977.html']
    post_extract = LxmlLinkExtractor(
        allow=(
            '/\d+.html',
            '/nofresh/\d+',
            'mop\.com/\d+'
        ),
        allow_domains=(
            'dzh.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )
    #个人主页里的个人资料
    author_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+/profile',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    author_page_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    fans_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+/fans',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    friends_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+/follow',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/s/[0-9]+',
        # ),
        allow_domains=(
            'dzh.mop.com'
        ),
        # deny=(
        #     '/print.html'
        # ),
        # deny_domains=(
        #     'q.blog.sina.com.cn'
        # )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(fans_extract, follow=True, callback='parse_fans'),
        Rule(friends_extract, follow=True, callback='parse_friends'),
        Rule(author_page_extract, follow=True),
        Rule(post_extract, follow=True, callback='parse_post'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
    )

    a_p_count = 0
    a_count = 0
    p_count = 0
    f_count = 0

    # def parse_page(self, response):
    #     self.a_p_count += 1
    #     print('author page: ', self.a_p_count, '  ', response.url)

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)
        author_id = author_item['author_id']

        data_param = 'data=%7B"header"%3A%7B%7D%2C"req"%3A%7B"User%2FSubCount"%3A%7B"uid"%3A"' + \
                     author_id + '"%7D%2C"User%2FSnsCount"%3A%7B"uid"%3A"' + author_id + '"%7D%7D%7D'

        data_url = 'http://hi.mop.com/ajax/get?' + data_param

        yield Request(
            url=data_url,
            callback=self.parse_author_data,
            method='POST',
            meta={
                'author_item': author_item
            },
            priority=10,
        )

    def parse_author_data(self, response):
        author_item = response.meta['author_item']
        data_json = response.text
        try:
            json_obj = json.loads(data_json)
            if json_obj:
                friends_num = json_obj['resp']['User/SnsCount']['retObj']['follow']
                author_item['friends_num'] = friends_num

                fans_num = json_obj['resp']['User/SnsCount']['retObj']['fans']
                author_item['fans_num'] = fans_num

                post_num = json_obj['resp']['User/SubCount']['retObj']['subject']
                author_item['post_num'] = post_num

                reply_num = json_obj['resp']['User/SubCount']['retObj']['reply']
                author_item['reply_num'] = reply_num
        finally:
            yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item,uuid = get_post_item(response)
        comment_data_url_code = get_comment_data(response)
        data_url = 'http://comment.mop.com/mopcommentapi/dzh/replylist/api/v170828/replyat/offset/asc/'+comment_data_url_code+'/0/100'
        #data_url = 'http://comment.mop.com/mopcommentapi/dzh/replylist/api/v170828/replyat/offset/asc/1514090902288858977/82/10'
        yield Request(
            url=data_url,
            callback=self.parse_comments,
            meta={
                'post_item': post_item,
                'uuid':uuid
                # 'page':1,
                # 'comment_data_url_code':comment_data_url_code
            },
            priority=10,
        )
        # post_id = post_item['post_id']
        #
        # for comment_item in get_comment_item(response, post_id):
        #     post_item['comment_ids'].append(comment_item['comment_id'])
        #
        #     yield comment_item
        #
        # yield post_item
#19.16
    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)
    def parse_comments(self, response):
        post_item = response.meta['post_item']
        uuid = response.meta['uuid']
        # page = response.meta['page']
        # comment_data_url_code = response.meta['comment_data_url_code']
        data_json = response.text
        try:
            json_obj = json.loads(data_json)
            if json_obj:
                comment_list = json_obj['data']
                for i in comment_list:
                    comment_item = CommentItem()
                    comment_item['post_id'] = post_item['post_id']
                    comment_item['comment_id'] = i['id']
                    post_item['comment_ids'] = post_item['comment_ids']+i['id']+','
                    comment_item['user_id'] = i['userid']
                    comment_item['user_href'] = 'http://hi.mop.com/space/' + i['userid'] + '/'
                    comment_item['user_name'] = i['username']
                    comment_item['date_time'] = unix_to_time(i['replytime'])
                    body = i['body']
                    html = etree.HTML(body)
                    content = html.xpath('string(.)')
                    comment_item['content'] = str(content)
                    images = html.xpath('//img/@src')
                    picture_hrefs=''
                    for i in images:
                        picture_hrefs=picture_hrefs+i+'|'
                    comment_item['picture_hrefs'] = picture_hrefs
                    comment_item['picture_path'] = ''
                    comment_item['praise_num'] = str(i['praisenum'])
                    comment_item['reply_num'] = str(i['subreplynum'])
                    comment_item['floor_num'] = i['floor']
                    yield comment_item

        except:
            pass

            # data_url = 'http://comment.mop.com/mopcommentapi/dzh/replylist/api/v170828/replyat/offset/asc/'+comment_data_url_code+'/'+str(page*100)+'/100'
            # yield Request(
            #     url=data_url,
            #     callback=self.parse_comments,
            #     meta={
            #         'post_item': post_item,
            #         'page': 1,
            #         'comment_data_url_code': comment_data_url_code
            #     },
            #     priority=10,
            # )
            # page+=1
        unix = time_to_unix()
        data_url = 'http://staticize.mop.com/subject/getArticleById?callback=jQuery18305051216432884662_'+\
            unix+'0&id='+uuid+'&type=dzh&_='+unix+'1'
        yield Request(
            url=data_url,
            callback=self.parse_post_data,
            meta={
                'post_item': post_item,
            },
            priority=20,
        )
    def parse_post_data(self, response):
        post_item = response.meta['post_item']
        data_json = response.text
        str=data_json
        a = re.compile(r'"replynum":\w+,')
        b = re.compile(r'"readnum":\w+,')
        c = re.compile(r'"praisenum":\w+,')
        d = re.compile(r'"recommendnum":\w+,')
        e = re.compile(r'"favoritenum":\w+,')
        replynum = re.search(a, str).group().split(':')[-1].split(',')[0]
        readnum = re.search(b, str).group().split(':')[-1].split(',')[0]
        praisenum = re.search(c, str).group().split(':')[-1].split(',')[0]
        recommendnum = re.search(d, str).group().split(':')[-1].split(',')[0]
        favoritenum = re.search(e, str).group().split(':')[-1].split(',')[0]
        post_item['reply_num'] = replynum
        post_item['hits'] = readnum
        post_item['praise_num'] = praisenum
        post_item['recommend_num'] = recommendnum
        post_item['collect_num'] = favoritenum
        yield post_item
    def parse_fans(self, response):
        sel = Selector(response)
        user_id = sel.xpath('//div[@class="hpUserInfo1"]/@uid').extract_first()

        fans_list = get_fans_item(response)
        for fans_id, fans_url in fans_list:
            fans_item = FansItem()
            fans_item['fans_id'] = fans_id
            fans_item['friends_id'] = user_id

            yield fans_item
            yield Request(
                url=fans_url + '/profile',
                callback=self.parse_author
            )

    def parse_friends(self, response):
        sel = Selector(response)
        user_id = sel.xpath('//div[@class="hpUserInfo1"]/@uid').extract_first()

        friends_list = get_fans_item(response)
        for friends_id, friends_url in friends_list:
            fans_item = FansItem()
            fans_item['fans_id'] = user_id
            fans_item['friends_id'] = friends_id

            yield fans_item
            yield Request(
                url=friends_url + '/profile',
                callback=self.parse_author
            )
