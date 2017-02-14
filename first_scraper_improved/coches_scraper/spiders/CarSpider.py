import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from coches_scraper.items import CarItem, CarItemLoader


class CarSpider(CrawlSpider):

    name = 'coches.net'
    start_urls = ["http://www.coches.net/segunda-mano/?or=1&fi=oTitle"]

    rules = ( 
        Rule(LinkExtractor(restrict_xpaths='//a[@class="mt-CardAdDate"]'),
            callback ='scrape_car_page'),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="mt-Pagination-link mt-Pagination-link--next "]'))
    )


    critical_fields = ('title', 'price')
    error_fields = ('year', 'seats', 'area', 'horse_power', 'transmission', 'doors', 'km', 'image_urls')
    all_fields = ('title', 'price', 'year', 'fuel', 'seats', 'area', 'insurance', 'color', 'horse_power',
                  'transmission', 'doors', 'km', 'description', 'image_urls', 'extra_equipment')

    def scrape_fields(self, response):

        
        data = {
            'title': response.xpath('//strong[@class="t-h2 mt-AdDetailHeader-title"]/text()').extract_first(),
            'price': response.xpath('//span[@class="t-h1 mt-AdDetailHeader-price u-c--red"]/text()').extract_first(),
            'year': response.xpath('//li[@class="mt-DataGrid-item"][1]/b/text()').extract_first(),
            'seats': response.xpath('//li[@class="mt-DataGrid-item"][6]/b/text()').extract_first(),
            'area': response.xpath('//li[@class="mt-DataGrid-item"][3]/b/text()').extract_first(),
            'horse_power': response.xpath('//li[@class="mt-DataGrid-item"][7]/b/text()').extract_first(),
            'transmission': response.xpath('//li[@class="mt-DataGrid-item"][4]/b/text()').extract_first(),
            'color': response.xpath('//li[@class="mt-DataGrid-item"][8]/b/text()').extract_first(),
            'doors': response.xpath('//li[@class="mt-DataGrid-item"][5]/b/text()').extract_first(),
            'km': response.xpath('//li[@class="mt-DataGrid-item"][2]/b/text()').extract_first(),
            'description': response.xpath('//section[@class="u-mb--xlarge"]/p/text()').extract_first()
        }


        data_list = response.xpath('//li/b/text()').extract()
        if len(data_list) == 9:
            data['fuel'] = data_list[8]
        elif len(data_list) == 10:
            data['fuel'] = data_list[9]
        elif len(data_list) == 11:
            data['fuel'] = data_list[9]
            data['insurance'] = data_list[10]

        if response.xpath('//div[@id="PhotoSlider"]//a/@href').extract_first() is not None:
            data['image_urls'] = response.xpath('//div[@id="PhotoSlider"]//a/@href').extract()

        if response.xpath('//ul[@id][@class="mt-List"]/li/text()').extract_first() is not None:
            data['extra_equipment'] = response.xpath('//ul[@id][@class="mt-List"]/li/text()').extract()
        elif response.xpath('//ul[@class="listachecks"]/li/text()').extract_first() is not None:
            data['extra_equipment'] = response.xpath('//ul[@class="listachecks"]/li/text()').extract()

        return data

    def check_missing_fields(self, data, url):

        for field in data.keys():
            if not data[field]:
                if field in self.critical_fields:
                    logging.critical('Required Field Not Found\t Field Name : {}\tUrl : {}'.format(field, url))
                elif field in self.error_fields:
                    logging.error('Important Field Not Found\t Field Name : {}\tUrl : {}'.format(field, url))
                else:
                    logging.warning('Data Field Not Found\tField Name : {}\tUrl : {}'.format(field, url))
                

    def scrape_car_page(self, response):
        """ This tests the page structure

        @url http://www.coches.net/nissan-pulsar-15dci-110cv-acenta-5p-diesel-2016-en-murcia-32370891-covo.aspx
        @returns items 1
        @scrapes year seats area horse_power transmission doors km image_urls 
        """
        car = CarItemLoader(item=CarItem(), response=response)

        data = self.scrape_fields(response)
        self.check_missing_fields(data, response.url)

        for key, value in data.items():
            car.add_value(key, value)

        yield car.load_item()

