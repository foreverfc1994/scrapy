#!/usr/bin python3
# -*- coding:utf-8 -*-
from scrapy import Selector
from doubanGroup import settings
import urllib.request
from lxml import etree
from doubanGroup.items import PostItem
from doubanGroup.spiders.group import get_group_id_by_href

check_value = lambda x: x if x else ''


def get_post_item(response):
    url = response.url
    print(url)
    sel = Selector(response)
    post_item = PostItem()
    post_item['url'] = url

    post_id = sel.xpath('//div[@class="sns-bar-fav"]/a/@data-tid').extract_first()
    post_item['post_id'] = check_value(post_id)

    group_name = sel.xpath('//div[@class="group-item"]/div[@class="info"]/div[@class="title"]/a/text()').extract_first()
    post_item['group_name'] = check_value(group_name)

    group_href = sel.xpath('//div[@class="group-item"]/div[@class="info"]/div[@class="title"]/a/@href').extract_first()
    post_item['group_href'] = check_value(group_href)

    group_id = get_group_id_by_href(group_href)
    post_item['group_id'] = check_value(group_id)

    pic_src = sel.xpath('//div[@class="user-face"]/a/img[@class="pil"]/@src').extract_first()
    post_item['author_id'] = get_author_id_by_head_src(pic_src)

    author_name = sel.xpath('//span[@class="from"]/a/text()').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_href = sel.xpath('//span[@class="from"]/a/@href').extract_first()
    post_item['author_href'] = check_value(author_href)

    title = sel.xpath('//div[@id="content"]/h1/text()').extract_first()
    post_item['title'] = check_value(title).strip()

    date_time = sel.xpath('//span[@class="color-green"]/text()').extract_first()
    post_item['date_time'] = check_value(date_time)

    content = sel.xpath('//div[@id="link-report"]/div[@class="topic-content"]').xpath('string(.)').extract_first()
    post_item['content'] = check_value(content)

    picture_hrefs = sel.xpath('//div[@id="link-report"]/div[@class="topic-content"]//img/@src').extract()
    post_item['picture_hrefs'] = [response.urljoin(pic_href) for pic_href in picture_hrefs if pic_href]
    # post_item['recommend_num'] = sel.xpath('//')
    post_item['recommend_num'] = get_rec_num(url)
    post_item['like_num'] = get_like_num(url)
    # recommend_num = sel.xpath('//div[@class="rec-sec"]/span[@class="rec-num"]/text()').extract_first()
    # if recommend_num and len(recommend_num) > 1:
    #     post_item['recommend_num'] = recommend_num[:-1]
    # else:
    #     post_item['recommend_num'] = '0'
    #
    # like_num = sel.xpath('//div[@class="sns-bar-fav"]/span[@class="fav-num"]/a/text()').extract_first()
    # if like_num and len(like_num) > 1:
    #     post_item['like_num'] = like_num[:-1]
    # else:
    #     post_item['like_num'] = '0'

    post_item['comment_ids'] = []

    return post_item


def get_author_id_by_head_src(pic_src):
    print(pic_src)
    pic_name = pic_src.split('/')[-1]

    author_id = '_'
    if pic_name:
        u_id = pic_name.split('-')[0]
        if u_id:
            author_id = u_id[1:]

    return author_id
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}

header=settings.DEFAULT_REQUEST_HEADERS_1
def get_likenum_by_url(url):
    req = urllib.request.Request(url,headers=header)
    res = urllib.request.urlopen(req).read().decode()
    html = etree.HTML(res)
    list=html.xpath('//div[@class="list topic-fav-list"]/ul/li')
    return len(list)
def get_recnum_by_url(url):
    req = urllib.request.Request(url,headers=header)
    res = urllib.request.urlopen(req).read().decode()
    html = etree.HTML(res)
    list=html.xpath('//div[@class="list topic-rec-list"]/ul/li')
    return len(list)
def get_rec_num(url):
    rec_num = 0
    i=1
    rec_url=url+'?type=rec#sep'
    req = urllib.request.Request(rec_url,headers=header)
    res = urllib.request.urlopen(req).read().decode()
    html = etree.HTML(res)
    is_page=html.xpath('//div[@class="paginator"]')
    num = len(html.xpath('//div[@class="list topic-rec-list"]/ul/li'))
    rec_num += num
    if is_page:
        page_num=html.xpath('//div[@class="paginator"]/a/text()')[-1]
        while i<int(page_num):
            page_url=url+'?type=like&start='+str(i*100)+'#sep'
            this_page_num=get_recnum_by_url(page_url)
            rec_num+=this_page_num
            i+=1
    else:
        pass
    return rec_num

def get_like_num(url):
    like_num = 0
    i=1
    like_url=url+'?type=like#sep'
    req = urllib.request.Request(like_url,headers=header)
    res = urllib.request.urlopen(req).read().decode()
    html = etree.HTML(res)
    is_page=html.xpath('//div[@class="paginator"]')
    num = len(html.xpath('//div[@class="list topic-fav-list"]/ul/li'))
    like_num += num
    if is_page:
        page_num=html.xpath('//div[@class="paginator"]/a/text()')[-1]
        while i<int(page_num):
            page_url=url+'?type=rec&start='+str(i*100)+'#sep'
            this_page_num=get_likenum_by_url(page_url)
            like_num+=this_page_num
            i+=1
    else:
        pass
    return like_num