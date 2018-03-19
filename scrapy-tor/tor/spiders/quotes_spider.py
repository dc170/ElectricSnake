import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://msydqstlz2kzerdg.onion/address/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
	fn = open("tor_map.txt","a")
        title = response.xpath('//title/text()').extract()[0]
        url = response.request.url
	fn.write(title+";"+url+",")
        print title
	print url
	fn.close()
        next_page_url = response.xpath('//li[@class="hs_site clickable_pointer"]/h3/a/@href').extract()
        if next_page_url is not None:
           for page in next_page_url:
              yield scrapy.Request(page)
