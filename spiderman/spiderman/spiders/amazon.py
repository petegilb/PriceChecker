# -*- coding: utf-8 -*-
import scrapy
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        'https://www.amazon.com/s?k=smartphone&crid=IVYWLZTQKNT1&sprefix=%2Caps%2C200&ref=nb_sb_ss_i_1_0'
    ]

    def parse(self, response):
        for item in response.css('div.s-result-item'):
            yield {
                'name': item.css('h2 span::text').extract(),
                'img': item.css('img.s-image::attr(src)').extract(),
                'price': item.css('span.a-price span.a-offscreen::text').extract_first(default='Not Found!'),
            }

        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
