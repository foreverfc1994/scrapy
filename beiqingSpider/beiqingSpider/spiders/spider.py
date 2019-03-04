from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from beiqingSpider.spiders.news import get_news_item
class BQSpider(CrawlSpider):
    name = 'beiqing'
    allowed_domains = ['ynet.com',
                       'report.ynet.com',
                       'youth.ynet.com',
                       'ent.ynet.com',
                       'finance.ynet.com',
                       'sports.ynet.com',
                       'life.ynet.com'
                       'culture.ynet.com',
                       'home.ynet.com',
                       'auto.ynet.com',
                       'ly.ynet.com']
    start_urls = ['http://www.ynet.com/',
                  'http://ly.ynet.com/',
                  'http://auto.ynet.com/',
                  'http://home.ynet.com/',
                  'http://culture.ynet.com/',
                  'http://life.ynet.com/',
                  'http://sports.ynet.com/',
                  'http://ent.ynet.com/',
                  'http://youth.ynet.com/',
                  'http://report.ynet.com/',
                  'http://news.ynet.com/']
    new_extract = LxmlLinkExtractor(
        allow=(
            '/\d+/\d\d/\d\d/\d+\w\d+.html'
        ),
        allow_domains = (
            'news.ynet.com',
            'youth.ynet.com',
            'report.ynet.com',
            'ent.ynet.com',
            'finance.ynet.com',
            'life.ynet.com',
            'culture.ynet.com',
            'home.ynet.com',
            'auto.ynet.com',
            'ly.ynet.com',
        )
    )
    follow_extract = LxmlLinkExtractor(
        allow = (
            '/w+.html'
        ),
        allow_domains = (
            'news.ynet.com',
            'youth.ynet.com',
            'report.ynet.com',
            'ent.ynet.com',
            'finance.ynet.com',
            'life.ynet.com',
            'culture.ynet.com',
            'home.ynet.com',
            'auto.ynet.com',
            'ly.ynet.com',

        )
    )
    rules = (
        Rule(new_extract,follow=True,callback='parse_news'),
        Rule(follow_extract,follow=True)
    )
    def parse_news(self,response):
        new_item = get_news_item(response)
        sel = Selector(response)
        ispage = sel.xpath('//*[@id="articleAll"]/ul')
        if ispage:
            next_url = new_item['url'].replace('.html','_2.html')
            page_num = len(sel.xpath('//*[@id="articleAll"]/ul/li'))
            yield Request(
                url=next_url,
                callback=self.parse_next_page,
                meta={
                    'new_item':new_item,
                    'page_num':page_num

                },
            )
        else:
            yield new_item
    def parse_next_page(self, response):
        new_item = response.meta['new_item']
        page_num = response.meta['page_num']
        sel = Selector(response)
        active_page = int(response.url.split('_')[-1].split('.')[0])
        if active_page<page_num:
            content_data = sel.xpath('//*[@id="articleBox"]').xpath('.//p')
            content = ''
            for p in content_data:
                content = content + p.xpath('string(.)').extract_first() + '\n'
            new_item['content'] = new_item['content']+content
            picture_list = sel.xpath('//*[@id="articleBox"]').xpath('.//img')
            picture_href = ''
            for i in picture_list:
                picture_href = picture_href + i.xpath('./@src').extract_first() + ','
            new_item['picture_href'] = new_item['picture_href'] + picture_href
            next_url = response.url.replace('_'+str(active_page),'_'+str(active_page+1))
            yield Request(
                url=next_url,
                callback=self.parse_next_page,
                meta={
                    'new_item': new_item,
                    'page_num': page_num
                },
            )
        else:
            yield new_item
        pass