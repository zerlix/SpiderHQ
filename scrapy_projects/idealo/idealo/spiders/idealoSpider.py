import scrapy
import json
from scrapy.http import HtmlResponse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

##
# Artikelübesichtsseiten
# https://www.idealo.de/preisvergleich/ProductCategory/26888.html


class SeleniumMiddleware:
    def __init__(self):
        #self.driver = webdriver.Chrome()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)


class IdealospiderSpider(scrapy.Spider):
    name = "idealoSpider"
    allowed_domains = ["idealo.de"]
    start_urls = ["https://www.idealo.de/preisvergleich/OffersOfProduct/202310657_-wan28k43-bosch.html",
                  "https://www.idealo.de/preisvergleich/OffersOfProduct/203244595_-nem-creme-classic-300ml-arko.html",
                  "https://www.idealo.de/preisvergleich/OffersOfProduct/201836903_-le-beau-eau-de-parfum-jean-paul-gaultier.html"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
        'idealo.spiders.idealoSpider.SeleniumMiddleware' : 1
        }
    }
        
    def parse(self, response):
        try:
            with open('tmp/output.html', 'wb') as f:
                f.write(response.body)
        except Exception as e:
            self.log(f'Error while writing file: {e}')
            
        script = response.xpath('//script[contains(., "@context")]/text()').get()
        data = json.loads(script)
        ean = data.get('gtin')
        price = data['offers']['lowPrice']
        print({'ean': ean, 'price': price})


    def parse_data(self,response):
        pass