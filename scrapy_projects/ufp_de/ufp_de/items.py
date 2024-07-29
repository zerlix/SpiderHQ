# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtikelItem(scrapy.Item):
    Artikelname = scrapy.Field(output_processor=str)
    EAN = scrapy.Field(output_processor=int) 
    Marke = scrapy.Field(output_processor=str)
    OEM = scrapy.Field(output_processor=str)
    Kapazitaet = scrapy.Field(output_processor=str)
    Fuellmenge = scrapy.Field(output_processor=str)
    Farbe = scrapy.Field(output_processor=str)
    Produktinformationen = scrapy.Field(output_processor=str)
    Model_list = scrapy.Field(output_processor=str)
    Url = scrapy.Field(output_processor=str)
    Image = scrapy.Field(output_processor=str)

