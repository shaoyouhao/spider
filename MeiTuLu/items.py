# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituluItem(scrapy.Item):
    # define the fields for your item here like:
    img_type = scrapy.Field()
    jigou = scrapy.Field()
    mote = scrapy.Field()
    biaoqian = scrapy.Field()
    img_name = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
