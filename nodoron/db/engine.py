from functools import lru_cache

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session

from nodoron.db.base import Base


def get_engine():
    settings = get_project_settings()
    db_settings = settings.get('DATABASE')
    if not db_settings:
        raise RuntimeError('Missing DATABASE settings')
    return create_engine(URL(**db_settings))


@lru_cache()
def get_session() -> Session:
    return sessionmaker(bind=get_engine())()


def create_db():
    Base.metadata.create_all(get_engine())
