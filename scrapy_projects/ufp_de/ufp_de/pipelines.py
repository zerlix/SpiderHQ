# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ArtikelItem
from src.database.MariaDB import MariaDatabase as Database

class UfpDePipeline:
    
    def __init__(self):
        self.db = Database()
    
    def open_spider(self, spider):
        self.db.connect()
        self.db.create_table(spider.name ,
                """EAN VARCHAR(14) PRIMARY KEY, 
                   Artikelname VARCHAR(255),
                   Marke VARCHAR(255),
                   OEM VARCHAR(255),
                   Kapazitaet VARCHAR(255),
                   Fuellmenge VARCHAR(255),
                   Farbe VARCHAR(255),
                   Produktinformationen TEXT,
                   Model_list TEXT,
                   Url VARCHAR(255),
                   Image VARCHAR(255)""")
        spider.logger.info(f"SQL-Abfrage: CREATE TABLE IF NOT EXISTS {spider.name}")
        
            
    def process_item(self, item, spider):
        if isinstance(item, ArtikelItem):
            
            if item['EAN']:
                item_dict = dict(item)
                if item_dict['Model_list']:
                    item_dict['Model_list'] = [model.replace('(', '').replace(')', '') for model in item_dict['Model_list']]
                    item_dict['Model_list'] = ', '.join(item_dict['Model_list'])
                else:
                    item_dict['Model_list'] = None
                    
                self.db.insert_update(spider.name, item_dict, 'EAN')
                spider.logger.info(f"Eintrag in {spider.name} gespeichert")
                return item
            else:
                spider.logger.error(f"Kein EAN gefunden")
        return item
