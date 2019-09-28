# -*- coding: utf-8 -*-
from logging import Logger

import scrapy
from nodoron.exceptions import ResponseNotAsExceptedException
from json import loads
from json.decoder import JSONDecodeError
import re
from nodoron.items import ApartmentItem
import datetime as dt
from nodoron.config import SEARCH_URLS

YAD2_VIEW_ITEM_URL = 'https://www.yad2.co.il/item/{item_id}'




class Yad2RentSpider(scrapy.Spider):
    RESPONSE_FIELDS = ['price', 'street', 'address_home_number', 'neighborhood',
                       'merchant', 'date_added', 'square_meters', 'city']

    name = "yad2_rent"
    start_urls = list(map(str, SEARCH_URLS))

    def start_requests(self):
        self.logger.info("Starting search...")
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            json_response = loads(response.body_as_unicode())
            raw_items = json_response['feed']['feed_items']
        except (KeyError, JSONDecodeError):
            message = "Response from page {0} is not as expected. The request might have " \
                      "been blocked".format(response.url)
            self.logger.exception()
            raise ResponseNotAsExceptedException(message)

        for raw_item in raw_items:

            apartment = ApartmentItem()
            if not (raw_item.get('id') and raw_item.get('price')):
                continue

            for key in self.RESPONSE_FIELDS:
                apartment[key] = raw_item.get(key)

            yad2_id = raw_item['id']
            apartment['yad2_id'] = yad2_id
            self.log(f'Found entry {yad2_id}')

            # Price comes formatted like '5,000 ₪', we extract the digits.
            apartment['price'] = ''.join([char for char in apartment['price'] if char.isdigit()])
            apartment['coordinates_latitude'] = raw_item['coordinates']['latitude']
            apartment['coordinates_longitude'] = raw_item['coordinates']['longitude']
            if raw_item.get('date_added'):
                apartment['date_added'] = dt.datetime.strptime(apartment['date_added'], '%Y-%m-%d %H:%M:%S')
            apartment['rooms'] = raw_item['Rooms_text']
            apartment['title'] = raw_item['title_1']
            yield apartment

        # Next page
        paginator = json_response['paginator']
        if paginator['last_page'] > paginator['current_page']:
            next_page = paginator['current_page'] + 1
            yield response.follow(re.sub(r'page=(\d+)', 'page={0}'.format(next_page), response.url),
                                  callback=self.parse)
