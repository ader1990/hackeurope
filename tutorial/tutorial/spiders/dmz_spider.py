from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["scj.ro"]

    def start_requests(self):
        yield Request(url='http://www.scj.ro/dosare.asp?', method="GET")

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath("//*[@cellspacing=1]").extract()
        print sites