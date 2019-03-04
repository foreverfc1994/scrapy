from scrapy import Selector
import re
from jingbaoSpider.items import newsItem
from jingbaoSpider.MD5Utils import md5_code
check_value = lambda x: x if x else ''
def get_news_item(response):
    url = response.url
    id = url.split('/')[-1].split('.')[0]
    md5 = md5_code(id).encode()
    sel = Selector(response)
    condition1 = sel.xpath('//*[@id="toolbar"]/span')
    condition2 = sel.xpath('//*[@id="fullpage"]/div/div/div/div[@class="redline"]')
    news_Item = newsItem()
    news_Item['url'] = url
    news_Item['id'] = id
    news_Item['md5'] = md5
    if condition1:
        news_Item = get_common_data(news_Item,sel)
        content, picture_href = condition_one(sel,url)
        news_Item['content'] = content
        news_Item['picture_href'] = picture_href
        countPage, currentPage = get_pages(sel)
        print(1)
        print(news_Item['url'])
        return news_Item,countPage,currentPage,'1'
    elif condition2:
        news_Item = get_common_data(news_Item, sel)
        content, picture_href = condition_two(sel, url)
        news_Item['content'] = content
        news_Item['picture_href'] = picture_href
        countPage, currentPage = get_pages(sel)
        print(2)
        print(news_Item['url'])
        return news_Item, countPage, currentPage, '2'
    else:
        print(3)
        print(news_Item['url'])
        news_Item = condition_three(news_Item,sel)
        countPage, currentPage = get_pages(sel)
        return news_Item, countPage, currentPage, '3'
def condition_one(sel,url):
    txt_mian = sel.xpath('//div[@class="maintxt"]'
                        '/div[@id="sourceTxt"]')
    content_data = txt_mian.xpath('.//p')
    content = ''
    for p in content_data:
        content = content+p.xpath('string(.)').extract_first()+'\n'
    picture_data = txt_mian.xpath('.//img/@src').extract()
    picture_href = ''
    base_href = url.replace(url.split('/')[-1],'')
    for pic in picture_data:
        picture_href = picture_href+base_href+pic.replace('./','')+','
    # news_Item['picture_path'] = picture_path
    #md5 = md5_code(id).encode()
    return content,picture_href


    pass
def condition_two(sel,url):
    txt_mian = sel.xpath('//div[@class="maintxt"]'
                         '/div[@class="TRS_Editor"]')
    content_data = txt_mian.xpath('.//p')
    content = ''
    for p in content_data:
        content = content + p.xpath('string(.)').extract_first() + '\n'
    picture_data = txt_mian.xpath('.//img/@src').extract()
    picture_href = ''
    base_href = url.replace(url.split('/')[-1], '')
    for pic in picture_data:
        picture_href = picture_href + base_href + pic.replace('./', '') + ','
    return content,picture_href
def get_common_data(news_Item,sel):
    title = sel.xpath('//div[@class="maintxt"]'
                      '/div[@class="tit"]/text()').extract_first().strip()
    publish_time = sel.xpath('//div[@class="maintxt"]/div[@class="info"]/span[1]/text()').extract_first()
    resource = sel.xpath('//div[@class="maintxt"]/div[@class="info"]/span[2]/text()').extract_first()
    editor = sel.xpath('//div[@class="maintxt"]/div[@class="info"]/span[3]/text()').extract_first()
    category = sel.xpath('//div[@class="ad"]/text()').extract_first()
    news_Item['category'] = category
    news_Item['resource'] = resource
    news_Item['title'] = title
    news_Item['publish_time'] = publish_time
    news_Item['editor'] = editor
    picture_path = ''
    news_Item['picture_path'] = picture_path
    return news_Item
def get_pages(sel):
    count = sel.xpath('//div[@class="changePage"]').xpath('string(.)').extract_first()
    com = r'var countPage = \d+'
    com2 = r'var currentPage = \d+'
    countPage = int(re.findall(com, count)[0].split(' = ')[-1])
    currentPage = int(re.findall(com2, count)[0].split(' = ')[-1]) + 1
    return countPage,currentPage
def condition_three(news_Item,sel):
    url = news_Item['url']
    title = sel.xpath('//*[@id="fullpage"]/div/div/div/div[2]'
                      '/div[@class="tit"]').xpath('string(.)').extract_first().strip()
    publish_time = sel.xpath('//*[@id="fullpage"]/div/div/div/div[2]/div[@class="info"]/span[1]/text()').extract_first()
    resource = sel.xpath('//*[@id="fullpage"]/div/div/div/div[2]/div[@class="info"]/span[2]/text()').extract_first()
    editor = sel.xpath('//*[@id="fullpage"]/div/div/div/div[2]/div[@class="info"]/span[3]/text()').extract_first()
    category = sel.xpath('//div[@class="the_ad"]/a[2]/text()').extract_first()
    news_Item['category'] = category
    news_Item['resource'] = resource
    news_Item['title'] = title
    news_Item['publish_time'] = publish_time
    news_Item['editor'] = editor
    picture_path = ''
    news_Item['picture_path'] = picture_path
    txt_mian = sel.xpath('//*[@id="fullpage"]/div/div/div/div[4]/div[1]/div'
                         '/div[@class="TRS_Editor"]')
    content_data = txt_mian.xpath('.//p')
    content = ''
    for p in content_data:
        content = content + p.xpath('string(.)').extract_first() + '\n'
    picture_data = txt_mian.xpath('.//img/@src').extract()
    picture_href = ''
    base_href = url.replace(url.split('/')[-1], '')
    for pic in picture_data:
        picture_href = picture_href + base_href + pic.replace('./', '') + ','
    news_Item['content'] = content
    news_Item['picture_href'] = picture_href
    return news_Item

