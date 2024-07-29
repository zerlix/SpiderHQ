from scrapy import signals
import random

class RandomUserAgentMiddleware:
    ''' gibt zu jedem Request einen zufälligen User-Agent zurück
        Kann in der settings.py aktiviert werden um zufällige User-Agent zu verwenden 
        DOWNLOADER_MIDDLEWARES = {
            "ebakery.ScrapyRandomAgentMiddleware.RandomUserAgentMiddleware": 544,
        }
    '''
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
