from geopy.distance import geodesic


class GeoFilter:
    def __init__(self, latitude, longitude, max_distance_km):
        self.latitude = latitude
        self.longitude = longitude
        self.max_distance_km = max_distance_km

    def get_distance_in_km(self, latitude, longitude):
        return geodesic((self.latitude, self.longitude), (latitude, longitude)).km

    def is_in_max_distance(self, latitude, longitude):
        return self.get_distance_in_km(latitude, longitude) <= self.max_distance_km
