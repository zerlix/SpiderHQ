# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SoldbergItem(scrapy.Item):
    # define the fields for your item here like:
    sku = scrapy.Field()
    images = scrapy.Field()