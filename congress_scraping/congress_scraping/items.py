# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose


# def to_lower(x):
#     return x.lower()


class Senate(scrapy.Item):
    # define the fields for your item here like:
    
    name = scrapy.Field()
    picture = scrapy.Field()
    party = scrapy.Field()
    birth_date = scrapy.Field()
    city = scrapy.Field()
    com_const = scrapy.Field()
    twitter = scrapy.Field()

    pass

