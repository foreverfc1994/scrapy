from scrapy import Request
from scrapy import Selector
import json
from dongfangSpider.items import newsItem,commentItem
from dongfangSpider.spiders.news import get_news_item
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
import sys
sys.setrecursionlimit(1000000)
class DFSpider(CrawlSpider):
    name = 'dongfang'
    # allowed_domains =['mini.eastday.com',
    #                   # 'mil.eastday.com'
    #                   ]
    # redis_key = "dongfangspider:start_urls"
    start_urls = ['http://mini.eastday.com/']
    news_extract = LxmlLinkExtractor(
        allow=(
            '/\w/\d+.html'
        ),
        allow_domains = (
                        'mini.eastday.com',

                    ),
    )
    follow_extract = LxmlLinkExtractor(
        allow_domains=(
            'mini.eastday.com',
            'mil.eastday.com'
        ),
    )
    rules = (Rule(news_extract,follow=True,callback='parse_news'),
             Rule(follow_extract,follow=True,callback='parse_follow'),
             )
    def parse_news(self, response):
        news_Item,countPage,currentPage= get_news_item(response)
        news_Item1= news_Item
        if not currentPage==countPage:
            url = news_Item['url']
            next_url = url.replace('.html', '-' + str(currentPage + 1) + '.html')
            yield Request(
                url=next_url,
                callback=self.parse_next_page,
                meta={
                    'news_Item': news_Item,
                    'countPage': countPage
                },
                priority=10,

            )
        else:
            comment_url = 'http://aboutcomment.dftoutiao.com/comment/api/tt/pc/' \
                          +news_Item['id']+'/commentreply?rowkey='+news_Item['id']+'&revnum=10&endkey=0&limitnum=200'
            yield Request(
                url=comment_url,
                callback=self.parse_comments,
                meta={
                    'news_Item': news_Item1,
                },
                priority=10,
            )
            # yield news_Item1
    def parse_follow(self, response):
        print('follow:'+response.url)
    def parse_next_page(self, response):
        news_Item = response.meta['news_Item']
        countPage = response.meta['countPage']
        sel =Selector(response)
        text_data = sel.xpath('//div[@class="J-contain_detail_cnt contain_detail_cnt"]')
        content_data = text_data.xpath('.//p')
        content = ''
        for p in content_data:
            content = content + p.xpath('string(.)').extract_first() + '\n'
        news_Item['content'] = news_Item['content']+content
        picture_data = text_data.xpath('.//img/@src').extract()
        picture_href = ''
        for pic in picture_data:
            picture_href = picture_href + pic + ','
        news_Item['picture_href'] = news_Item['picture_href']+picture_href
        currentPage = int(sel.xpath('//div[@class="pagination"]/a[@class="cur"]/text()').extract_first())
        news_Item1 = news_Item
        if not currentPage==countPage:
            url = news_Item['url']
            next_url = url.replace('.html', '-' + str(currentPage + 1) + '.html')
            yield Request(
                url=next_url,
                callback=self.parse_next_page,
                meta={
                    'news_Item': news_Item,
                    'countPage': countPage
                },
                priority=10,

            )
            #yield news_Item
        else:
            comment_url = 'http://aboutcomment.dftoutiao.com/comment/api/tt/pc/' \
                          + news_Item['id'] + '/commentreply?rowkey=' + news_Item[
                              'id'] + '&revnum=10&endkey=0&limitnum=200'
            yield Request(
                url=comment_url,
                callback=self.parse_comments,
                meta={
                    'news_Item': news_Item1,
                },
                priority=10,
            )
            # yield news_Item1
    def parse_comments(self, response):
        new_Item = response.meta['news_Item']
        data_json = response.text.replace('null(','').replace(');','')
        json_obj = json.loads(data_json)
        data = json_obj['data']
        comment_count = len(data)
        new_Item['comment_count'] = str(comment_count)
        for comment in data:
            comment_Item = commentItem()
            author_name = comment['username']
            created_time = comment['date']
            author_id = comment['userid']
            news_id = comment['aid']
            content = comment['content']
            zan_count = comment['ding']
            comment_Item['author_name'] = author_name
            comment_Item['created_time'] = created_time
            comment_Item['author_id'] = author_id
            comment_Item['news_id'] = news_id
            comment_Item['content'] = content
            comment_Item['zan_count'] = zan_count
            new_Item['comment_ids'] = new_Item['comment_ids']+author_id+','
            yield comment_Item
        yield new_Item

