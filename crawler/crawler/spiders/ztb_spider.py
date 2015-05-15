import scrapy
import operator

from crawler.items import NewsItem
from crawler.items import CrawlerItem

class ZtbSpider(scrapy.Spider):
	name = "ztb"
	allowed_domains = ["http://ztb.kz"]
	start_urls = ["http://ztb.kz"]

	def parse(self, response):
		print "starting to parse ZTB"
		items = []
		def getComments(item):
			return int(item['num_comments'])

		for sel in response.xpath('//div[@class="span6 entry-preview"]'):
			item = NewsItem()
			item['title'] = sel.xpath('h3/a/text()')[0].extract()
			item['url'] = self.allowed_domains[0] + sel.xpath('a/@href')[0].extract()
			item['num_comments'] = sel.xpath('ul/li/text()')[1].extract()
			items.append(item)

		# sort in descending order by number of comments
		items.sort(key=getComments, reverse=True)
		for item in items[:5]:
			yield(item)
