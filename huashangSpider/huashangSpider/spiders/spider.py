from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from huashangSpider.spiders.news import get_news_item
class HSspider(RedisCrawlSpider):
    name = 'huashang'
    # allowed_domains =['news.hsw.cn']
    redis_key = "huashangspider:start_urls"
    # start_urls = ['http://news.hsw.cn/']
    news_extract = LxmlLinkExtractor(
        allow=(
            '/system/\d+/\d+/\d+.shtml\w*'),
        allow_domains=(
            'xy.hsw.cn',
            'fun.hsw.cn',
            'news.hsw.cn'
        )
    )
    follow_extract = LxmlLinkExtractor(
        allow_domains=(
            'xy.hsw.cn',
            'fun.hsw.cn',
            'news.hsw.cn'
        ),
        allow=(
            '/tpxw08/\w*',
            '/shhot/\w*',
            '/gjhot/\w*',
            '/glhot/\w*',
            '/hszb/\w*',
            '/xwzt08/',
            '/sx08/xaxw08/\w*',
            '/sx08/\w*',
            # '/\w*'
        ),
        deny=('/system/\d+/\d+/\d+.shtml\w*')
    )
    rules = (
        Rule(news_extract,follow=True,callback='parse_news'),
        Rule(follow_extract,follow=True,callback='parse_follows'),
    )
    def parse_news(self, response):
        news_Item,page,currentpage = get_news_item(response)
        new_Item = news_Item
        if page == currentpage:
            print('B')
            yield news_Item
        else:
            next_url = new_Item['url'].replace('.shtml','_'+str(currentpage+1)+'.shtml')
            yield Request(
                url=next_url,
                callback=self.parse_next_page,
                meta={
                    'news_Item':new_Item,
                    'page':page
                },
                priority = 10,
            )
    def parse_follows(self, response):
        print('follow:'+response.url)
    def parse_next_page(self, response):
        news_Item = response.meta['news_Item']
        page = response.meta['page']
        sel = Selector(response)
        txt_data = sel.xpath('//div[@class="photoarea"]')
        content_data = txt_data.xpath('.//p')
        content_ = ''
        for p in content_data:
            content_ = content_ + p.xpath('string(.)').extract_first() + '\n'
        try:
           content = content_.split('相关热词搜索：')[0]
        except:
            content = content_
        news_Item['content'] = news_Item['content']+content
        picture_data = txt_data.xpath('.//img/@src').extract()
        picture_href = ''
        for pic in picture_data:
            picture_href = picture_href + pic + ','
        news_Item['picture_href'] = news_Item['picture_href'] + picture_href
        currentpage = int(response.url.split('/')[-1].split('.shtml')[0].split('_')[-1])
        new_Item = news_Item
        if currentpage==page:
            print('A')
            yield news_Item
        else:
            next_url = new_Item['url'].replace('.shtml', '_' + str(currentpage + 1) + '.shtml')
            print('next')
            yield Request(
                url=next_url,
                callback=self.parse_next_page,
                meta={
                    'news_Item': new_Item,
                    'page': page
                },
                priority=10,
            )
        pass
