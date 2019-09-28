# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApartmentItem(scrapy.Item):
    yad2_id = scrapy.Field()
    price = scrapy.Field()
    city = scrapy.Field()
    coordinates_latitude = scrapy.Field()
    coordinates_longitude = scrapy.Field()
    street = scrapy.Field()
    address_home_number = scrapy.Field()
    neighborhood = scrapy.Field()
    merchant = scrapy.Field()
    date_added = scrapy.Field()
    square_meters = scrapy.Field()
    rooms = scrapy.Field()
    title = scrapy.Field()
