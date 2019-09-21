from sqlalchemy import Column, Integer, String, create_engine, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from scrapy.utils.project import get_project_settings

Base = declarative_base()


class ApartmentModel(Base):
    __tablename__ = 'apartments'
    id = Column(String(10), primary_key=True, unique=True)
    price = Column(Integer)
    coordinates_latitude = Column(Float)
    coordinates_longitude = Column(Float)
    street = Column(String(1024))
    address_home_number = Column(Integer)
    neighborhood = Column(String(1024))
    merchant = Column(Boolean)
    date_added = Column(DateTime)
    square_meters = Column(Integer)
    view_url = Column(String(1024))
    rooms = Column(Integer)
    title = Column(String(1024))


# CREATE THE DB FOR THE FIRST TIME
if __name__ == '__main__':
    settings = get_project_settings()
    db_settings = settings.get('DATABASE')
    if not db_settings:
        raise RuntimeError('Missing DATABASE settings')
    engine = create_engine(URL(**db_settings))
    Base.metadata.create_all(engine)

