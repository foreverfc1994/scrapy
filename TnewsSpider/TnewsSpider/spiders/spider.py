from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
import json
import re
from TnewsSpider.items import commentItem,newsItem,replyItem
from TnewsSpider.spiders.news import get_news_item,unix_to_time
class Tspider(CrawlSpider):
    name = 'tnews'
    start_urls = ['http://news.qq.com/',
                  'http://news.qq.com/articleList/rolls/',
                  'http://news.qq.com/world_index.shtml']
    news_extract = LxmlLinkExtractor(
        allow=(
            '/a/\w+',
               # '/omn/\w+',
               # '/omn/\d+/\w+.html',
               # '/omn/\d+/\w+'
               '/a/\w+#\w+'
               ),
        allow_domains=(
            'mil.qq.com',
            'new.qq.com',
            # 'ent.qq.com',
            # 'sports.qq.com',
            'finance.qq.com',
            'tech.qq.com',
            'edu.qq.com',
            # 'house.qq.com'
        )

    )
    follow_extract = LxmlLinkExtractor(
        allow_domains=(
            'mil.qq.com',
            'new.qq.com',
            # 'ent.qq.com',
            # 'sports.qq.com',
            'finance.qq.com',
            'tech.qq.com',
            'edu.qq.com',
            # 'house.qq.com'
        ),
        # deny=(
        #     ' /omn/\w+'
        # )
    )
    rules = (
        Rule(news_extract,follow=True,callback='parse_news'),
        Rule(follow_extract,follow=True,callback='parse_follow')
    )
    def parse_news(self, response):
        #print('news:'+response.url)
        newsitem,cmt_id=get_news_item(response)
        if cmt_id=='0':
             yield newsitem
        else:
            yield newsitem
            cmt_url = 'http://coral.qq.com/article/'\
                      +cmt_id+'/comment/v2?orinum=1000&oriorder=t&pageflag=1&cursor=0&scorecursor=0&source=1&orirepnum=1000&reporder=o&reppageflag=1&_=1517736161719'
            yield Request(
                url=cmt_url,
                callback=self.parse_comment,
            )
            # cmt_url = 'http://coral.qq.com/article/'+str(cmt_id)+'/commentnum?callback=_article'+str(cmt_id)+'commentnum&_=1517732503501'
            # yield Request(
            #     url=cmt_url,
            #     callback=self.parse_cmtcount,
            #     meta={
            #         'newsitem':newsitem,
            #         'cmt_id':cmt_id
            #     }
            # )



    def parse_follow(self, response):
        pass
        #print('follow:' + response.url)
    def parse_comment(self, response):
        data = response.text
        json_data = json.loads(data)
        datas = json_data['data']
        hasnext = datas['hasnext']
        commentlist = datas['oriCommList']
        targetid = str(datas['targetid'])
        for comm in commentlist:
            commentitem = commentItem()
            commentitem['targetid'] = comm['targetid']
            commentitem['created_time'] = unix_to_time(comm['time'])
            commentitem['userid'] = comm['userid']
            commentitem['content'] = comm['content']
            commentitem['up'] = comm['up']
            commentitem['replynum'] = comm['orireplynum']
            commentitem['id'] = comm['id']
            yield commentitem
        replylist = datas['repCommList']
        if replylist:
            for key in replylist.keys():
                replys = replylist[key]
                for reply in replys:
                    replyitem = replyItem()
                    replyitem['targetid'] = reply['targetid']
                    replyitem['parent'] = reply['parent']
                    replyitem['created_time'] = unix_to_time(reply['time'])
                    replyitem['userid'] = reply['userid']
                    replyitem['content'] = reply['content']
                    replyitem['up'] = reply['up']
                    replyitem['id'] = reply['id']
                    yield replyitem
        else:
            pass

        if not hasnext:
            pass
        else:
            last = datas['last']
            cmt_url = 'http://coral.qq.com/article/' \
                      + targetid + '/comment/v2?orinum=1000&oriorder=t&pageflag=1&cursor='+last+'&scorecursor=0&source=1&orirepnum=1000&reporder=o&reppageflag=1&_=1517736161719'
            yield Request(
                url=cmt_url,
                callback=self.parse_comment,
            )
    def parse_cmtcount(self, response):
        html = response.text
        newsitem = response.meta['newsitem']
        cmt_id = response.meta['cmt_id']
        cp = r'"commentnum":"\d+"'
        cmt_count = re.findall(r'\d+',re.findall(cp,html)[0])[0]

        a=1
