# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from siteModel.models import News
from scrapy.exceptions import DropItem

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        try:
            item.save()
        except:
            print "Could not save an item"
