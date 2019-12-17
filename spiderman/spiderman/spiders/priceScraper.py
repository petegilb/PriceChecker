import scrapy

class AmazonScraper(scrapy.Spider):
    name = 'price'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/'
    ]

    def parse(self, response):
        pass
