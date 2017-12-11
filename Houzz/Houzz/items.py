# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouzzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    project_info = scrapy.Field()
    project_name = scrapy.Field()
    project_url = scrapy.Field()
    img_bigUrl = scrapy.Field()
    img_link = scrapy.Field()
    designer_name = scrapy.Field()
    img_collection = scrapy.Field()
    img_name = scrapy.Field()
    relevant_theme = scrapy.Field()
    img_Category = scrapy.Field()
    img_Keywords = scrapy.Field()
