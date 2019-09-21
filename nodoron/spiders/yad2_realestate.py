# -*- coding: utf-8 -*-

import scrapy
from nodoron.exceptions import ResponseNotAsExceptedException
from json import loads
from json.decoder import JSONDecodeError
import re
from nodoron.items import ApartmentItem
import datetime as dt
from nodoron.config import SEARCH_URLS
from nodoron.utils.telegram_bot import send_starting_search_message, send_error_message

YAD2_VIEW_ITEM_URL = 'https://www.yad2.co.il/item/{item_id}'


class Yad2RentSpider(scrapy.Spider):
    RESPONSE_FIELDS = ['id', 'price', 'street', 'address_home_number', 'neighborhood',
                       'merchant', 'date_added', 'square_meters']

    name = "yad2_rent"
    start_urls = list(map(str, SEARCH_URLS))

    def start_requests(self):
        send_starting_search_message()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            json_response = loads(response.body_as_unicode())
            items = json_response['feed']['feed_items']
        except (KeyError, JSONDecodeError):
            message = "Response from page {0} is not as expected. The request might have " \
                      "been blocked".format(response.url)
            send_error_message(message)
            raise ResponseNotAsExceptedException(message)

        for item in items:

            apartment = ApartmentItem()
            if not (item.get('id') and item.get('price')):
                continue

            for key in self.RESPONSE_FIELDS:
                apartment[key] = item.get(key)

            item_id = apartment['id']
            self.log('Found entry %s' % item_id)

            # Price comes formatted like '5,000 ₪', we extract the digits.
            apartment['price'] = ''.join([char for char in apartment['price'] if char.isdigit()])
            apartment['coordinates_latitude'] = item['coordinates']['latitude']
            apartment['coordinates_longitude'] = item['coordinates']['longitude']
            if item.get('date_added'):
                apartment['date_added'] = dt.datetime.strptime(apartment['date_added'], '%Y-%m-%d %H:%M:%S')
            apartment['view_url'] = YAD2_VIEW_ITEM_URL.format(item_id=item_id)
            apartment['rooms'] = item['Rooms_text']
            apartment['title'] = item['title_1']
            yield apartment

        # Next page
        paginator = json_response['paginator']
        if paginator['last_page'] > paginator['current_page']:
            next_page = paginator['current_page'] + 1
            yield response.follow(re.sub(r'page=(\d+)', 'page={0}'.format(next_page), response.url),
                                  callback=self.parse)
