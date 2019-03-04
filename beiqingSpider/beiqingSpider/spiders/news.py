from scrapy import Selector

from beiqingSpider.items import newsItem
from beiqingSpider.MD5Utils import md5_code
check_value = lambda x: x if x else ''
def get_news_item(response):
    url = response.url
    sel = Selector(response)
    news_Item = newsItem()
    news_Item['url'] = url
    id = url.split('/')[-1].split('.')[0].split('_')[0]
    news_Item['id'] = id
    title = sel.xpath('//div[@class="articleTitle"]/h1/text()').extract_first()
    news_Item['title'] = title
    publish_time_year = sel.xpath('//span[@class="yearMsg"]/text()').extract_first()
    publish_time_time = sel.xpath('//span[@class="timeMsg"]/text()').extract_first()
    publish_time = publish_time_year+' '+publish_time_time
    news_Item['publish_time'] = publish_time
    resource = sel.xpath('//span[@class="sourceMsg"]/text()').extract_first()
    news_Item['resource'] = resource
    category = sel.xpath('//dl[@class="cfix fLeft"]/dt/a/text()').extract_first()
    news_Item['category'] = category
    content_data = sel.xpath('//*[@id="articleBox"]').xpath('.//p')
    content = ''
    for p in content_data:
        content=content+p.xpath('string(.)').extract_first()+'\n'
    news_Item['content'] = content
    picture_list = sel.xpath('//*[@id="articleBox"]').xpath('.//img')
    picture_href=''
    for i in picture_list:
        picture_href = picture_href+i.xpath('./@src').extract_first()+','
    news_Item['picture_href'] = picture_href
    news_Item['picture_path'] = ''
    editor = sel.xpath('//*[@id="articleBox"]/span/text()').extract_first()
    news_Item['editor'] = editor
    md5 = md5_code(id).encode()
    news_Item['md5'] = md5
    return news_Item


