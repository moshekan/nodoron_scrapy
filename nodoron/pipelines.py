# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

from nodoron.db import Apartment, get_session
from .utils.telegram_bot import send_new_apartment_message
from.utils.yad2_api import get_phone_list


class ApartmentSQLitePipeline:
    def __init__(self):
        settings = get_project_settings()
        self.database = settings.get('DATABASE')
        self.session = get_session()

    def process_item(self, item, spider):
        yad2_id = item.get('yad2_id')
        if self.does_exist_in_db(yad2_id):
            raise DropItem(f"Item {yad2_id} is already in database")
        apartment_model = Apartment(**item)
        self.session.add(apartment_model)
        self.session.commit()
        return item

    def does_exist_in_db(self, yad2_id):
        return self.session.query(Apartment.id).filter_by(yad2_id=yad2_id).scalar() is not None
