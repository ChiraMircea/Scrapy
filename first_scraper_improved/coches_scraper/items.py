import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

class CarItemLoader(ItemLoader):

    default_input_processor = MapCompose(unicode.strip)

class CarItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    year = scrapy.Field()
    seats = scrapy.Field()
    area = scrapy.Field()
    horse_power = scrapy.Field()
    insurance = scrapy.Field()
    fuel = scrapy.Field()
    transmission = scrapy.Field()
    color = scrapy.Field()
    doors = scrapy.Field()
    km = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    extra_equipment = scrapy.Field()
