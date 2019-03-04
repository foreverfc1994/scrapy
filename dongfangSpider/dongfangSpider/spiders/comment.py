from scrapy import Selector
import re
from dongfangSpider.items import newsItem,commentItem
check_value = lambda x: x if x else ''