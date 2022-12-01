import scrapy
import json
import os.path
import html
import unicodedata
import uuid

def get_json_urls():
    f = open(os.path.dirname(__file__) + '/../../links.json')
    data = json.load(f)
    urls = []
    for link_object in data:
        urls.append(link_object['link'])
    f.close()
    return urls
def filter_name(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    no_accents = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    no_accents = no_accents.replace(" Subscription", "").replace("BARREL COFFEE SERIES - ", "")
    decoded = bytes(no_accents, "utf-8").decode("unicode_escape").strip()
    return decoded
def filtered_details_list(input_arr, target_attr):
    return {
        'amount' : input_arr[0].split(" of beans ")[0],
        'location': input_arr[0].split(" of beans from ")[1].split(",")[0]

    }

class CoffeeSpider(scrapy.Spider):
    name = "coffee"
    start_urls = get_json_urls()

    def parse(self, response):
        filtered_coffee_name = filter_name(response.css('h1.ProductItem-details-title::text').get())
        image_link = response.css('img.ProductItem-gallery-slides-item-image::attr(data-image)').get()
        price = response.css('div.product-price::text').get().split(" ")[1]
        raw_details = response.css('div.ProductItem-details-excerpt').css('p::text').getall()
        details_object = filtered_details_list(raw_details)

        yield {
            'id': uuid.uuid1().int,
            'name': filtered_coffee_name,
            'price': price,
            'image_link' : image_link,
        }