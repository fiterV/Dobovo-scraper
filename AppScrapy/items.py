# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    housingArea = scrapy.Field()
    minAmountOfNights = scrapy.Field()
    floor = scrapy.Field()
    berthCount = scrapy.Field()
    bathroomCount = scrapy.Field()
    owner = scrapy.Field()
    personalSpeaks = scrapy.Field()
    additionalAdvantages = scrapy.Field()
    minSum = scrapy.Field()
    freeDates = scrapy.Field()
    address = scrapy.Field()
    mark = scrapy.Field()


