from scrapy import Selector
import re
from dongfangSpider.items import newsItem,commentItem
from dongfangSpider.MD5Utils import md5_code
from bs4 import BeautifulSoup
check_value = lambda x: x if x else ''
def get_news_item(response):
    url = response.url
    id = url.split('/')[-1].split('.')[0]
    md5= md5_code(id)
    sel = Selector(response)
    news_Item = newsItem()
    news_Item['url'] = url
    news_Item['id'] = id
    news_Item['md5'] = md5
    title = sel.xpath('//div[@class="J-title_detail title_detail"]/h1/span/text()').extract_first()
    news_Item['title'] = title
    publish_time = sel.xpath('//div[@class="share_cnt_p clearfix"]/div[@class="fl"]/i[1]/text()').extract_first()
    news_Item['publish_time'] = publish_time

    resource = sel.xpath('//div[@class="share_cnt_p clearfix"]/div[@class="fl"]/i[2]/text()').extract_first()

    soup = BeautifulSoup(response.text,'html.parser')
    resource2 = soup.find_all('div', class_='fl')[0].contents[-2].string
    # com = r'target="_blank">[\u4e00-\u9fa5]+</a>'
    #resource2 = sel.xpath('/html/body/div[12]/div/div[2]/div[2]/div/div[1]/div/p/a/text()').extract_first()
    if resource:
        news_Item['resource'] = resource
    else:
        news_Item['resource'] = resource2
    text_data = sel.xpath('//div[@class="J-contain_detail_cnt contain_detail_cnt"]')
    content_data = text_data.xpath('.//p')
    content = ''
    for p in content_data:
        content = content+p.xpath('string(.)').extract_first()+'\n'
    news_Item['content'] = content
    picture_data = text_data.xpath('.//img/@src').extract()
    picture_href = ''
    for pic in picture_data:
        picture_href = picture_href+pic+','
    news_Item['picture_href'] = picture_href
    category = sel.xpath('//div[@class="detail_position"]/a[2]/text()').extract_first().strip()
    news_Item['category'] = category
    try:
        tags = ''
        tags_data = sel.xpath('//ul[@class="tagcns"]/li')
        for tag in tags_data:
            a = tag.xpath('a/text()').extract_first()
            tags = tags+a+' '
        news_Item['tags'] = check_value(tags)
    except:
        news_Item['tags'] = ''
    print(url)
    # i=sel.xpath('//div[@class="pagination"]').xpath('string(.)').extract_first()
    # print(i)
    # a = soup.find_all('div', class_='pagination')[0]
    # b = a.find_all('a')
    # for i in b:
    #     print(i.string)
    currentPage = int(sel.xpath('//div[@class="pagination"]/a[@class="cur"]/text()').extract_first())
    countPage = 0
    try:
        if sel.xpath('//div[@class="pagination"]/a/text()').extract()[-1] == '下一页':
           countPage = int(sel.xpath('//div[@class="pagination"]/a/text()').extract()[-2])
        else:
            countPage = 1
    except Exception as e:
        pass
    picture_path = ''
    news_Item['picture_path'] = picture_path
    # print(countPage)
    # comment_count = sel.xpath('//span[@id="comment_num"]/text()').extract_first()
    # news_Item['comment_count'] = check_value(comment_count)
    news_Item['comment_ids'] = ''
    # print('pppp'+str(countPage))
    # print('cccc'+news_Item['comment_count'])
    return news_Item,countPage,currentPage
