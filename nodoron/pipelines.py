# -*- coding: utf-8 -*-

from .db_models import ApartmentModel
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from .config import GEO_FILTERS
from .utils.geo_filters import GeoFilter
from .utils.telegram_bot import send_new_apartment_message
from.utils.yad2_api import get_phone_list


class GeoFilterPipeLine:
    def process_item(self, item, spider):
        latitude = item['coordinates_latitude']
        longitude = item['coordinates_longitude']

        for geo_filter in GEO_FILTERS:
            if self.check_geo_filter(geo_filter, latitude, longitude):
                return item

        raise DropItem(f'Item {item["id"]} does not match any of the geo filters.')

    @staticmethod
    def check_geo_filter(geo_filter: GeoFilter, latitude, longitude):
        return geo_filter.is_in_max_distance(latitude, longitude)


class ApartmentSQLitePipeline:
    def __init__(self):
        settings = get_project_settings()
        self.database = settings.get('DATABASE')
        self.session = self.get_session()

    def process_item(self, item, spider):
        item_id = item.get('id')
        if self.is_item_exist(item_id):
            raise DropItem(f"Item {item_id} is already in database")
        apartment_model = ApartmentModel(**item)
        self.session.add(apartment_model)
        self.session.commit()

        return item

    def get_session(self):
        engine = create_engine(URL(**self.database))
        return sessionmaker(bind=engine)()

    def is_item_exist(self, item_id):
        return self.session.query(ApartmentModel.id).filter_by(id=item_id).scalar() is not None


class TelegramSenderPipeLine:
    def process_item(self, item, spider):
        phone_list = get_phone_list(item['id'])
        send_new_apartment_message(item, phone_list)
        return item
