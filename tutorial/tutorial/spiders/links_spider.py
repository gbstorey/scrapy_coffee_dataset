import scrapy

class LinksSpider(scrapy.Spider):
    name = "links"
    start_urls = [
        "https://www.infusioncoffeetea.com/coffee-subscriptions",
    ]
    def parse(self, response):
        for link in response.css('a.summary-title-link::attr(href)').getall():
            yield {
                'link': "https://www.infusioncoffeetea.com" + link
            }