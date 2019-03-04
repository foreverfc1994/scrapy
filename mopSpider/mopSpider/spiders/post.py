#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from mopSpider.items import PostItem

check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)
    url = response.url
    post_item = PostItem()
    post_item['url'] = url
    post_id = sel.xpath('//*[@id="filename"]/@value').extract_first()
    post_item['post_id'] = check_value(post_id)
    path_one = sel.xpath('//*[@id="mainplate"]/@value').extract_first()
    path_two = sel.xpath('//*[@id="subplate"]/@value').extract_first()
    if path_one and path_two:
        path_text = path_one+'/'+path_two
    elif path_one and not path_two:
        path_text = path_one
    else:
        path_text = path_two
    # path_div = sel.xpath('//p[contains(@class, "mt10")]/a[@title]')
    # path_href_list = path_div.xpath('./@href').extract()
    # path_text_list = path_div.xpath('./@title').extract()

    # post_item['path_text'] = ', '.join(path_text_list)
    # post_item['path_href'] = ', '.join([response.urljoin(path_href) for path_href in path_href_list])
    post_item['path_text'] = path_text
    path_href = sel.xpath('//div[@class="crumbs fl"]/a/@href').extract_first()
    post_item['path_href'] = path_href
    #title = sel.xpath('//h1[contains(@class, "subTitle")]').xpath('string(.)').extract_first()
    title = sel.xpath('//div[@class="post-header"]/h2/text()').extract_first()
    post_item['title'] = check_value(title)

    publish_date = sel.xpath('//div[@class="post-header-t"]/span/span[1]/text()').extract_first()
    post_item['publish_date'] = check_value(publish_date)

    hits = sel.xpath('//span[@class="post-click"]').xpath('string()').extract_first()
    post_item['hits'] = check_value(hits)

    reply_num = sel.xpath('//span[@class="post-reply"]/text()').extract_first()
    post_item['reply_num'] = check_value(reply_num)

    # author_id = sel.xpath('//div[@class="post-author-img fl"]')
    # post_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//div[@class="post-author-header"]/a[1]/text()').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_href = sel.xpath('//div[@class="post-author-header"]/a[1]/@href').extract_first()
    post_item['author_href'] = check_value(author_href)
    author_id = sel.xpath('//div[@class="post-author-img fl"]/@data-user-uid').extract_first()
    #author_id = author_href.split('/')[-1]
    post_item['author_id'] = check_value(author_id)
    contents = ''
    content = sel.xpath('//div[@class="detail-article"]').xpath('string(.)').extract_first()
    # for i in content:
    #     contents = content+i
    #content = contents.xpath('string(.)').extract_first()
    if content:
       content = content.split('__dzh__detail__renderGg__12();')[0].strip()

    post_item['content'] = check_value(content)

    images = sel.xpath('//div[@class="detail-article"]//img/@src').extract()
    picture_hrefs = ''
    for i in images:
        picture_hrefs = picture_hrefs+i+'|'
    post_item['picture_hrefs'] = picture_hrefs

    tags = sel.xpath('//div[@class="post-tags"]/a/text()').extract()
    tag = ''
    for i in tags:
        tag = tag+i+','
    post_item['tags'] = tag

    praise_num = sel.xpath('//div[@class="post-zan mr20 fl"]/em/text()').extract_first()
    if praise_num:
        post_item['praise_num'] = praise_num
    else:
        post_item['praise_num'] = '-1'

    recommend_num = sel.xpath('//div[@class="post-tj mr20 fl"]/em/text()').extract_first()
    if recommend_num:
        post_item['recommend_num'] = recommend_num
    else:
        post_item['recommend_num'] = '-1'

    collect_num = sel.xpath('//div[@class="post-sc mr20 fl"]/em/text()').extract_first()
    if collect_num:
        post_item['collect_num'] = collect_num
    else:
        post_item['collect_num'] = '-1'

    post_item['comment_ids'] = ''
    uuid = sel.xpath('//input[@id="articleid"]/@value').extract_first()
    return post_item,uuid
def get_comment_data(response):
    sel = Selector(response)
    url_a = sel.xpath('//input[@id="cts"]/@value').extract_first()
    url_b = sel.xpath('//input[@id="rdts"]/@value').extract_first()
    url = url_a+url_b
    return url