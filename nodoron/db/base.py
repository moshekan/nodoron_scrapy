from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def create_db():
    from nodoron.db.apartment_model import ApartmentModel
    from nodoron.db.request_location import RequestLocation
    from nodoron.db.search_request import SearchRequest
    settings = get_project_settings()
    db_settings = settings.get('DATABASE')
    if not db_settings:
        raise RuntimeError('Missing DATABASE settings')
    engine = create_engine(URL(**db_settings))
    Base.metadata.create_all(engine)


# CREATE THE DB FOR THE FIRST TIME
if __name__ == '__main__':
    create_db()
