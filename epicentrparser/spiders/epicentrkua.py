import scrapy
from scrapy.http import HtmlResponse
from epicentrparser.items import EpicentrparserItem
from scrapy.loader import ItemLoader


class EpicentrkuaSpider(scrapy.Spider):
    name = 'epicentrkua'
    allowed_domains = ['epicentrk.ua']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://epicentrk.ua/ua/shop/{kwargs.get('query')}/"]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='link link--big link--inverted link--blue']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=EpicentrparserItem(), response=response)

        loader.add_xpath('name', "//h1[@class='p-header__title nc']/text()")
        loader.add_xpath('name', "//div[@class='row head-panel product-head align-justify']/h1/text()")

        loader.add_xpath('price', "//div[@class='p-price__main']/text()")
        loader.add_xpath('price', "//span[@class='price-wrapper']/text()")

        loader.add_value('url', response.url)

        loader.add_xpath('photos', "//img[@class='p-slider__photo']/@src")
        loader.add_xpath('photos', "//img[contains(@class, 'swiper-lazy card-slider__top-image')]/@src")
        loader.add_xpath('photos', "//img[@class='product-single-image']/@src")

        yield loader.load_item()

