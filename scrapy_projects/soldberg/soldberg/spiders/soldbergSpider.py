import scrapy
from urllib.parse import urljoin, urlparse
import os
import requests

class SoldbergspiderSpider(scrapy.Spider):
    name = "soldbergSpider"
    allowed_domains = ["www.soldberg.de"]
    start_urls = ["https://www.soldberg.de/betten/?p=1", 
                  "https://www.soldberg.de/matratzen/?p=1",
                  "https://www.soldberg.de/lattenroste/?p=1",
                  "https://www.soldberg.de/decken/?p=1",
                  "https://www.soldberg.de/kissen/?p=1",
                  "https://www.soldberg.de/bettwaesche/?p=1",
                  "https://www.soldberg.de/moebel/?p=1",
                  "https://www.soldberg.de/garten/?p=1",
                  ]

    def parse(self, response):
        products = response.css('div.product--info')
        for product in products:
            # hole die Links zu den Artikel
            link = product.css('a::attr(href)').get()
            if link:
                yield response.follow(link, self.parse_data)
                
        # Folge der nächsten Seite
        next_page = response.css('a.paging--link.paging--next::attr(href)').get()
        if next_page:
            next_page_full = response.urljoin(next_page)
            current_url = response.url
            if next_page_full != current_url:
                self.logger.info(f"Next page: {next_page_full}")
                yield response.follow(next_page_full, self.parse)
        
        
    def parse_data(self, response):
        sku = response.xpath('//span[@itemprop="sku"]/text()').get()
        
        if sku:
            # Verarbeiten Sie die SKU-Nummer hier
            print(f"SKU: {sku}")
            sku = sku.strip()
        else:
            # Behandeln Sie den Fall, wenn keine SKU-Nummer gefunden wurde
            print("SKU nicht gefunden")
            return
        
        # Erstelle ein Verzeichnis für die SKU
        sku_dir = os.path.join("images", sku)
        os.makedirs(sku_dir, exist_ok=True)
        
        image_main = response.xpath('//span[@class="image--element"]//img/@src').get()
        if image_main:
            # Extrahiere den Dateinamen aus der URL
            parsed_url = urlparse(image_main)
            filename = os.path.basename(parsed_url.path)
            # Speichere das Bild im Verzeichnis
            image_path = os.path.join(sku_dir, filename)
            with open(image_path, "wb") as f:
                f.write(requests.get(image_main).content)
            print(f"Bild '{filename}' gespeichert in '{image_path}'")
        else:
            print("Keine Bild-URL (src) gefunden")
        
        image_extra = response.xpath('//div[@class="image--thumbnails image-slider--thumbnails productSlider"]//a[@class="thumbnail--link"]/img/@srcset').getall()
        base_url = response.url
        
        if image_extra:
            for url_set in image_extra:
                urls = url_set.split(', ')
                for url in urls:
                    url_parts = url.split(' ')
                    image_url = url_parts[0]
                    full_url = urljoin(base_url, image_url)
                
                    # Extrahiere den Dateinamen aus der URL
                    parsed_url = urlparse(full_url)
                    filename = os.path.basename(parsed_url.path)
                
                    # Speichere das Bild im Verzeichnis
                    image_path = os.path.join(sku_dir, filename)
                    with open(image_path, "wb") as f:
                        f.write(requests.get(full_url).content)
                        print(f"Bild '{filename}' gespeichert in '{image_path}'")
        else:
            print("Keine zusätzlichen Bild-URLs gefunden")
                    
                    
    