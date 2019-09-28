from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class SearchRequest(Base):

    __tablename__ = "search_requests"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chat_id = Column(String(20))
    min_price = Column(Integer)
    max_price = Column(Integer)
    city = Column(String(20))
    min_rooms = Column(Integer)
    max_rooms = Column(Integer)

    locations = relationship("RequestLocation", backref="search_request")
