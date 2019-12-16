import scrapy

class priceScraper(scrapy.Spider):
    name = 'example'
    allowed_domains = ['amazon.com']
    start_urls = ['']

    def parse(self, response):
        pass
