# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecordItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    bookname=scrapy.Field()
    author=scrapy.Field()
    rate=scrapy.Field()
    date=scrapy.Field()
    user_id=scrapy.Field()
    tag_url=scrapy.Field()

    pass
