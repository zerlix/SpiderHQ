import scrapy
import re
from ..items import ArtikelItem
 
# Artikelübersichtsseite
# https://www.ufp.de/de_DE/printer-supplies-inks/1240/?seq=priority-desc&page=1
# https://www.ufp.de/de_DE/printer-supplies-inks/1240/?seq=priority-desc&page=2
# usw..
#
# Artikelseite
# https://www.ufp.de/de_DE/p/n9k05ae-uus-hp-304-dj-ink-color-st-100-pages-2ml/57968/

class UfpSpider(scrapy.Spider):
    name = "ufpSpider"
    allowed_domains = ["ufp.de"]
    start_urls = ["https://www.ufp.de/de_DE/printer-supplies-inks/1240/?seq=priority-desc&page=1"]
    item = ArtikelItem()


    def parse(self, response):
        products = response.css('div.image')
        for product in products:
            # hole die Links zu den Artikel
            link = product.css('a::attr(href)').get()
            if link:
                yield response.follow(link, self.parse_data)
        
        # Folge der nächsten Seite
        next_page = response.css('li a:contains("Nächste")::attr(href)').get()
        if next_page:
            next_page_full = response.urljoin(next_page)
            current_url = response.url
            if next_page_full != current_url:
                self.logger.info(f"Next page: {next_page_full}")
                yield response.follow(next_page_full, self.parse)



    def parse_data(self, response):
        item = ArtikelItem()
        # EAN
        ean = response.xpath('//span[contains(text(), "EAN")]/following-sibling::span/text()').get()
        if ean:
            item['EAN'] = ean.strip()
        else:
            item['EAN'] = None
            
        # Hersteller
        marke = response.xpath('//span[contains(text(), "Marke")]/following-sibling::span/text()').get()
        if marke:
            item['Marke'] = marke.strip()
        else:
            item['Marke'] = None
            
        # OEM Code
        oem = response.xpath('//span[contains(text(), "OEM Code")]/following-sibling::span/text()').get()
        if oem:
            item['OEM'] = oem.strip()
        else:
            item['OEM'] = None
            
        # Kapazität
        kapazitaet = response.xpath('//span[contains(text(), "Kapazität (Seiten)")]/following-sibling::span/text()').get()
        if kapazitaet:
            item['Kapazitaet'] = kapazitaet.strip()
        else:
            item['Kapazitaet'] = None
        
        # Füllmenge in ml
        fuellmenge = response.xpath('//span[contains(text(), "Füllmenge")]/following-sibling::span/text()').get()
        if fuellmenge:
            item['Fuellmenge'] = fuellmenge.strip()
        else:
            item['Fuellmenge'] = None
        
        # Farbe
        farbe = response.xpath('//span[contains(text(), "Farbe")]/following-sibling::span/text()').get()
        if farbe:
            item['Farbe'] = farbe.strip()
        else:
            item['Farbe'] = None
                
        # Produktinformationen
        produktinformationen = response.css('div.description-paragraph').get()
        if produktinformationen:
            produktinformationen = re.sub('<.*?>', '', produktinformationen) # html tags entfernen
            produktinformationen = produktinformationen.replace('\n', '').replace('\r', '').strip() # leerzeichen, tabs etc..
            # Ersetzen der 3 Punkte gefolgt von unbekannte ANzahl an Leerzeichen durch ein Leerzeichen
            item['Produktinformationen'] = re.sub('\...\s+', ' ', produktinformationen)
        else:
            item['Produktinformationen'] = None
            
            
        # OEM vor dem  Artikelname entfernen
        item['Artikelname'] = response.css('h2.product-title::text').get()
        item['Artikelname'] = item['Artikelname'].replace(item['OEM'], '').strip()
        
        # Merkmale
        for ul in response.css('div.modal-body ul'):
            m = ul.css('li::text').getall()
            if m:
                item['Model_list'] = ul.css('li::text').getall()
            else:
                item['Model_list'] = None
                
        # url
        item['Url'] = response.url
        
        #image
        image = response.xpath('//div[contains(@class, "item active js-zoom-button")]/img/@src').get()
        if image:
            item['Image'] = image
        else:
            item['Image'] = None
        
        yield item
        
        
        