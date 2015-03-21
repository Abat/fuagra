#-*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field

from siteModel.models import News


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    pass


class NewsItem(DjangoItem):
    # fields for this item are automatically created from the django model
    django_model = News
