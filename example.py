import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["sandbox.oxylabs.io"]
    start_urls = ["https://sandbox.oxylabs.io"]

    def parse(self, response):
        pass
