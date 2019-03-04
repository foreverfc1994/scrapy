from scrapy import Request
from scrapy import Selector
from jingbaoSpider.spiders.news import get_news_item
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from jingbaoSpider.spiders.news import get_pages,condition_one,condition_two
class JBspider(CrawlSpider):
    name = 'jingbao'
    allowed_domains = ['bjd.com.cn',
                       'bj.bjd.com.cn',
                       'du.bjd.com.cn',
                       'v.bjd.com.cn',
                       '3j.bjd.com.cn']
    # zc / sbs / 201801 / 30 / t20180130_11079671.html
    start_urls=['http://www.bjd.com.cn/',
                'http://bj.bjd.com.cn/',
                'http://du.bjd.com.cn/'
                'http://v.bjd.com.cn/',
                'http://3j.bjd.com.cn/'
                ]
    new_extract = LxmlLinkExtractor(
        allow=(
           '/\w+/\w+/\d+/\d+/\w\d+_\d+.html',
           '/\w+/\d+/\d+/\w\d+_\d+.html'
        )
    )
    follow_extract = LxmlLinkExtractor(
        allow=(
            '/\w+/\w+/',
            '/\w+/\w+/index_\d+.html',
        )
    )
    rules = (
        Rule(new_extract,follow=True,callback='parse_news'),
        Rule(follow_extract,follow=True,callback='parse_follow'),
    )
    def parse_news(self, response):
        new_Item,countPage,currentPage,condition = get_news_item(response)
        if countPage == currentPage:
           yield new_Item
        else:
            next_page_url = new_Item['url'].replace('.html', '_' + str(currentPage) + '.html')
            yield Request(
                url=next_page_url,
                callback=self.parse_next_page,
                meta={
                    'news_item': new_Item,
                    'condition': condition
                }


            )


        pass
    def parse_next_page(self, response):
        sel = Selector(response)
        news_Item = response.meta['news_item']
        condition = response.meta['condition']
        url = news_Item['url']
        countPage=0
        currentPage=0
        if condition=='1':
            content, picture_href = condition_one(sel, url)
            news_Item['content'] = news_Item['content'] + content
            news_Item['picture_href'] = news_Item['picture_href'] + picture_href
            countPage, currentPage = get_pages(sel)
        elif condition=='2':
            content, picture_href = condition_two(sel, url)
            news_Item['content'] = news_Item['content'] + content
            news_Item['picture_href'] = news_Item['picture_href'] + picture_href
            countPage, currentPage = get_pages(sel)
        else:
            txt_mian = sel.xpath('//*[@id="fullpage"]/div/div/div/div[4]/div[1]/div'
                                 '/div[@class="TRS_Editor"]')
            content_data = txt_mian.xpath('.//p')
            content = ''
            for p in content_data:
                content = content + p.xpath('string(.)').extract_first() + '\n'
            news_Item['content'] = news_Item['content']+content
            picture_data = txt_mian.xpath('.//img/@src').extract()
            picture_href = ''
            base_href = url.replace(url.split('/')[-1], '')
            for pic in picture_data:
                picture_href = picture_href + base_href + pic.replace('./', '') + ','
            news_Item['picture_href'] = news_Item['picture_href'] + picture_href
            countPage, currentPage = get_pages(sel)
        if countPage == currentPage:
            yield news_Item
        else:
            next_page_url = news_Item['url'].replace('.html', '_' + str(currentPage) + '.html')
            yield Request(
                url=next_page_url,
                callback=self.parse_next_page,
                meta={
                    'news_item': news_Item,
                    'condition': condition
                }
            )


    # def parse_follow(self, response):
    #     print('follow',response)