import scrapy
# В settings.py добавляем:
from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS = ['--headless']

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}

# В пауке используем SeleniumRequest:
from scrapy_selenium import SeleniumRequest


def start_requests(self):
    yield SeleniumRequest(
        url='https://dynamic-site.com',
        callback=self.parse,
        wait_time=3  # Ждем 3 секунды для загрузки JavaScript
    )



class ExampleSpider(scrapy.Spider):
    name = "games"
    allowed_domains = ["sandbox.oxylabs.io"]
    start_urls = ["https://sandbox.oxylabs.io/products/"]

    def parse(self, response):
        yield {
            'genres': response.css('div.game-genres-wrapper css-mwff68 e1pl6npa9'),
            'rating': response.css('div.star-rating'),
            # 'rating': response.css('div.rating::attr(data-rating)').get('N/A'),
        }

        # Находим ссылку на следующую страницу и следуем по ней
    #
    # next_page = response.css('a.next-page::attr(href)').get()
    # if next_page:
    #     yield response.follow(next_page, self.parse)
