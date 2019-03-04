from scrapy import Selector
import re
from TnewsSpider.items import newsItem
from TnewsSpider.MD5Utils import md5_code
check_value = lambda x: x if x else ''
def get_news_item(response):
    url = response.url
    sel = Selector(response)
    if 'omn' in url:
        print(response.text)
        # get_classA_data(response)
        print('A')
    else:
        is_or_no = sel.xpath('//ul[@id="Smailllist"]')
        if not is_or_no:
            newsitem,cmt_id = get_classB_data(response)
            newsitem['url'] = url
            return newsitem,cmt_id

        else:
            pass
def get_classA_data(response):
    sel = Selector(response)
    id = response.url.split('/')[-1].split('.')[0]
    md5 = md5_code(id)
    newsitem = newsItem()
    title = sel.xpath('//title/text()').extract_first()
    category = ''
    class_ = '企鹅号'
    tags = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    html =response.text
    cp1 = r'"pubtime":"\w+",'
    publish_time = re.findall(cp1,html)[0].split('"')[-2]
    cp2 = r'"media":"[\u4e00-\u9fa5]+",'
    resource = re.findall(cp2,html)[0].split('"')[-2]
    txt_data = sel.xpath('//div[@class="content-article"]')
    ps= txt_data.xpath('.//p')
    content = ''
    for p in ps:
        a = p.xpath('string(.)').extract_first()
        script = p.xpath('.//script/text()').extract()
        style = p.xpath('.//style/text()').extract()
        for i in script:
            a=a.replace(i,'')
        for j in style:
            a=a.replace(j,'')
        content = content+a.replace('\n','').replace('\r','')+'\n'
    pictures = txt_data.xpath('.//img/@src').extract()
    picture_href = ''
    for pic in pictures:
        picture_href = picture_href + pic + ','
    newsitem['id'] = id
    newsitem['md5'] = md5
    newsitem['title'] = title
    newsitem['class_'] =class_
    newsitem['category'] = category
    newsitem['resource'] =resource
    newsitem['tags'] = tags
    newsitem['publish_time'] = publish_time
    newsitem['picture_href'] =picture_href
    newsitem['picture_path'] = ''
    newsitem['editor'] = ''
    newsitem['content'] = ''
    a= 1
    pass
def get_classB_data(response):
    sel = Selector(response)
    newsitem = newsItem()
    html = response.text
    try:
        cp1 = r'site_cname:\'[\u4e00-\u9fa5]+\','
        class_ = re.findall(cp1, html)[0].split('\'')[-2]
        newsitem['class_'] = class_
        cp2 = r'id:\'\d+\','
        id = re.findall(cp2, html)[0].split('\'')[-2]
        try:
            tagdata = sel.xpath('//div[@class="mark"]/span')
            tags = ''
            for tag in tagdata:
                tags = tags + tag.xpath('string(.)').extract_first() + ','
        except:
            tags = ''
        cp3 = r' cmt_id = \d+;'
        cmt = re.findall(cp3, html)[0]
        cmt_id = re.findall(r'\d+', cmt)[0]
        newsitem['targetid'] = cmt_id
        newsitem['tags'] = tags
        newsitem['id'] = id
        newsitem['md5'] = md5_code(id)
        title = sel.xpath('//div[@class="hd"]/h1/text()').extract_first()
        newsitem['title'] = check_value(title)
        category = sel.xpath('//div[@class="a_Info"]/span[@class="a_catalog"]').xpath('string(.)').extract_first()
        newsitem['category'] = check_value(category)
        resource = sel.xpath('//div[@class="a_Info"]/span[@class="a_source"]').xpath('string(.)').extract_first()
        newsitem['resource'] = check_value(resource)
        publish_time = sel.xpath('//div[@class="a_Info"]/span[@class="a_time"]').xpath('string(.)').extract_first()
        newsitem['publish_time'] = check_value(publish_time)
        # comment_count = sel.xpath('//em[@id="cmtNum"]/text()').extract_first()
        text_data = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]')
        ps = text_data.xpath('.//p')
        content = ''
        for p in ps:
            a = p.xpath('string(.)').extract_first()
            script = p.xpath('.//script/text()').extract()
            style = p.xpath('.//style/text()').extract()
            for i in script:
                a = a.replace(i, '')
            for j in style:
                a = a.replace(j, '')
            content = content + a.replace('\n', '').replace('\r', '') + '\n'
        newsitem['content'] = check_value(content)
        pictures = text_data.xpath('.//img/@src').extract()
        picture_href = ''
        for pic in pictures:
            picture_href = picture_href + pic + ','
        newsitem['picture_href'] = picture_href
        try:
            editor = sel.xpath('//div[@class="qq_editor"]/text()').extract_first().split('：')[-1]
        except:
            editor = 'wyxyzhang'
        newsitem['editor'] = editor
        newsitem['picture_path'] = ''
        newsitem['comment_num'] = '0'
        newsitem['comment_ids'] = ''
        return newsitem, cmt_id
    except:
        try:
            class_ = sel.xpath('//span[@bosszone="crumbNav"]/a[1]/text()').extract_first()
        except:
            class_ = ''
        try:
            category = sel.xpath('//span[@bosszone="crumbNav"]/a[2]/text()').extract_first()
        except:
            category = ''

        title = sel.xpath('//div[@class="hd"]/h1/text()').extract_first()
        publish_time = sel.xpath('//span[@class="pubTime"]/text()').extract_first().replace('年','-').replace('月','-').replace('日',' ')+':00'
        try:
            resource = sel.xpath('//span[@class="where"]/text()').extract_first()
        except:
            resource = ''
        cmt_id = '0'
        text_data = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]')
        ps = text_data.xpath('.//p')
        content = ''
        for p in ps:
            a = p.xpath('string(.)').extract_first()
            script = p.xpath('.//script/text()').extract()
            style = p.xpath('.//style/text()').extract()
            for i in script:
                a = a.replace(i, '')
            for j in style:
                a = a.replace(j, '')
            content = content + a.replace('\n', '').replace('\r', '') + '\n'
        newsitem['content'] = check_value(content)
        pictures = text_data.xpath('.//img/@src').extract()
        picture_href = ''
        for pic in pictures:
            picture_href = picture_href + pic + ','
        newsitem['picture_href'] = picture_href
        id = response.url.split('/')[-2]+response.url.split('/')[-1].split('.')[0]
        md5 = md5_code(id)
        editor = sel.xpath('//div[@class="QQeditor"]/text()').extract_first().split('：')[-1]
        newsitem['id'] = id
        newsitem['md5'] = md5
        newsitem['title'] = title
        newsitem['class_'] = class_
        newsitem['category'] = category
        newsitem['resource'] = resource
        newsitem['tags'] = ''
        newsitem['publish_time'] = publish_time
        newsitem['picture_path'] = ''
        newsitem['editor'] = editor
        return newsitem,cmt_id



    pass
import time
def unix_to_time(unix):
    a = int(unix)
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(a)
    dt = time.strftime(format, value)
    return dt
