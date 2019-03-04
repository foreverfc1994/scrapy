from scrapy import Selector
from huashangSpider.items import newsItem
from huashangSpider.MD5Utils import md5_code
check_value = lambda x: x if x else ''
def get_news_item(response):
    url = response.url
    id = url.split('/')[-1].split('.shtml')[0]
    sel = Selector(response)
    classA = sel.xpath('//div[@class="article-summary"]')
    if classA:
        news_Item = get_classA_data(sel)
        news_Item['url'] = url
        news_Item['id'] = id
        news_Item['md5'] = md5_code(id)
        return news_Item,1,1
    else:
        news_Item = get_classB_data(sel)
        news_Item['url'] = url
        news_Item['id'] = id
        news_Item['md5'] = md5_code(id)
        try:
            page = int(sel.xpath('//div[@id="news_more_page_div_id"]/a/text()').extract()[-4])
        except:
            page = 1
        return news_Item,page,1
def get_classA_data(sel):
    news_Item = newsItem()
    title = sel.xpath('//div[@class="article"]/div[@class="hd"]/h1/text()').extract_first()
    category = sel.xpath('//div[@class="origin"]/span[1]/a/text()').extract_first()
    resource = sel.xpath('//div[@class="origin"]//span[@class="ly-name"]/text()').extract_first()
    try:
        author = sel.xpath('//div[@class="origin"]/span[3]/span[1]/text()').extract_first().split('：')[-1]
    except:
        author = ''
    pulish_time = sel.xpath('//div[@class="origin"]//span[@class="article-time"]/text()').extract_first()
    abstract = sel.xpath('//div[@class="article-summary"]').xpath('string(.)').extract_first().replace('[摘要]','')
    txt_data = sel.xpath('//div[@class="contentBox cf"]')
    content_data = txt_data.xpath('.//p')
    content_ = ''
    for p in content_data:
        content_ = content_+p.xpath('string(.)').extract_first()+'\n'
    content = content_.split('编辑：')[0]
    editor = content_.split('编辑：')[1].replace('\n','')
    picture_data = txt_data.xpath('.//img/@src').extract()
    picture_href = ''
    for pic in picture_data:
        picture_href = picture_href+pic+','
    tag_data = sel.xpath('//div[@class="article"]/p[1]/a')
    tags = ''
    for tag in tag_data:
        tags = tags + tag.xpath('string(.)').extract_first()+' '
    # share_count = sel.xpath('//span[@class="jiathis_button_expanded jiathis_counter jiathis_bubble_style"]/text()').extract_first()
    news_Item['title'] = check_value(title)
    news_Item['author'] = check_value(author)
    news_Item['resource'] = check_value(resource)
    news_Item['category'] = check_value(category)
    news_Item['publish_time'] = check_value(pulish_time)
    news_Item['abstract'] = check_value(abstract)
    news_Item['content'] = check_value(content)
    news_Item['picture_href'] = check_value(picture_href)
    news_Item['picture_path'] = ''
    news_Item['editor'] = check_value(editor)
    news_Item['tags'] = check_value(tags)
    return news_Item

    pass
def get_classB_data(sel):
    news_Item = newsItem()
    title = sel.xpath('//div[@class="hd"]/h1/text()').extract_first()
    category1 = sel.xpath('//div[@class="breadcrumbs"]/span/a[2]/text()').extract_first()
    category2 = sel.xpath('//div[@class="breadcrumbs"]/span/a[3]/text()').extract_first()
    category = check_value(category1)+check_value(category2)
    try:
       resource = sel.xpath('//p[@class="origin"]//span[@id="source_baidu"]').xpath('string(.)').extract_first().split('：')[-1]
    except:
        resource = ''
    try:
        author = sel.xpath('//p[@class="origin"]//span[@id="author_baidu"]/text()').extract_first().split('：')[-1]
    except:
        author = ''
    pulish_time = sel.xpath('//p[@class="origin"]//span[@id="pubtime_baidu"]/text()').extract_first().split('：')[-1]
    abstract = ''
    txt_data = sel.xpath('//div[@class="photoarea"]')
    content_data = txt_data.xpath('.//p')
    content_ = ''
    for p in content_data:
        content_ = content_ + p.xpath('string(.)').extract_first() + '\n'
    try:
       content = content_.split('相关热词搜索：')[0]
       tags = content_.split('相关热词搜索：')[1]
    except:
        content = content_
        tags=''
    editor = sel.xpath('//p[@class="origin"]//span[@id="editor_baidu"]/text()').extract_first().split('：')[-1]
    picture_data = txt_data.xpath('.//img/@src').extract()
    picture_href = ''
    for pic in picture_data:
        picture_href = picture_href + pic + ','
    # tag_data = sel.xpath('//div[@class="article"]/p[1]/a')
    # tags = ''
    # for tag in tag_data:
    #     tags = tags + tag.xpath('string(.)').extract_first() + ' '

    # share_count = sel.xpath('//span[@id="jiathis_counter_47"]/text()').extract_first()
    news_Item['title'] = check_value(title)
    news_Item['author'] = check_value(author)
    news_Item['resource'] = check_value(resource)
    news_Item['category'] = check_value(category)
    news_Item['publish_time'] = check_value(pulish_time)
    news_Item['abstract'] = check_value(abstract)
    news_Item['content'] = check_value(content)
    news_Item['picture_href'] = check_value(picture_href)
    news_Item['picture_path'] = ''
    news_Item['editor'] = check_value(editor)
    news_Item['tags'] = check_value(tags)
    # news_Item['share_count'] = share_count
    return news_Item

    pass