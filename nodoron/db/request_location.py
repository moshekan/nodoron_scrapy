from sqlalchemy import Column, Integer, ForeignKey, Float

from nodoron.utils.geo_filters import GeoFilter
from .base import Base


class RequestLocation(Base):

    __tablename__ = "request_locations"

    request_location_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    search_request_id = Column(Integer, ForeignKey('search_requests.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    radius = Column(Float)

    def is_apartment_within_range(self, apartment):
        return GeoFilter(self.latitude, self.longitude, self.radius)\
            .is_in_max_distance(apartment.coordinates_latitude, apartment.coordinates_longitude)
