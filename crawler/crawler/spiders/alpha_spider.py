import scrapy

from crawler.items import NewsItem
from crawler.items import CrawlerItem

class AlphaSpider(scrapy.Spider):
    name = "alpha"
    allowed_domains = ["http://tengrinews.kz"]
    start_urls = ["http://tengrinews.kz"]
  
    def parse(self, response):
        for sel in response.xpath('//div[@id="discus_news"]/div/a'):
            #item = CrawlerItem()
            #item['title'] = sel.xpath('span[@class="name"]/text()').extract()[0]
            #item['link'] = self.allowed_domains[0] + sel.xpath('@href')[0].extract()
            #yield item 
            item = NewsItem()
            item['title'] = sel.xpath('span[@class="name"]/text()').extract()[0]
            item['url'] = self.allowed_domains[0] + sel.xpath('@href')[0].extract()
            yield item
