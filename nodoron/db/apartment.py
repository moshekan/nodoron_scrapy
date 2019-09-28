from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
import datetime as dt
from nodoron.spiders.yad2_realestate import YAD2_VIEW_ITEM_URL
from .base import Base


class Apartment(Base):

    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    yad2_id = Column(String(10), unique=True)
    price = Column(Integer)
    city = Column(String(20))
    coordinates_latitude = Column(Float)
    coordinates_longitude = Column(Float)
    street = Column(String(1024))
    address_home_number = Column(Integer)
    neighborhood = Column(String(1024))
    merchant = Column(Boolean)
    date_added = Column(DateTime)
    square_meters = Column(Integer)
    rooms = Column(Integer)
    title = Column(String(1024))
    create_date = Column(DateTime, default=dt.datetime.now)

    @property
    def view_url(self):
        return YAD2_VIEW_ITEM_URL.format(item_id=self.yad2_id)
