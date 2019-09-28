from sqlalchemy import Column, Integer, ForeignKey, DateTime
import datetime as dt

from sqlalchemy.orm import relationship

from nodoron.db.base import Base


class SentApartment(Base):

    __tablename__ = "sent_apartments"

    search_request_id = Column(Integer, ForeignKey('search_requests.id'), primary_key=True)
    apartment_id = Column(Integer, ForeignKey('apartments.id'), primary_key=True)
    sent_date = Column(DateTime, default=dt.datetime.now)

    search_request = relationship("SearchRequest", backref="sent_apartments")
    apartment = relationship("Apartment", backref="sent_apartments")
