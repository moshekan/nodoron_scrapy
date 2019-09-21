from .utils.yad2_api import Yad2ApiRealEstateWrapper, Range, City
from .utils.geo_filters import GeoFilter

SEARCH_URLS = [
    Yad2ApiRealEstateWrapper(rooms=Range(4, 6), price=Range(0, 7500), city=City.TEL_AVIV),
    Yad2ApiRealEstateWrapper(rooms=Range(4, 6), price=Range(0, 7500), city=City.HERZLIYA),
]

GEO_FILTERS = [
    # Tel aviv
    GeoFilter(32.103963, 34.803351, 0.5),  # Tel Aviv University Train Station
    GeoFilter(32.108510, 34.792238, 1.5),  # Ramat Aviv Alef
    GeoFilter(32.116657, 34.794643, 1.4),  # Neve Avivim
    GeoFilter(32.123046, 34.798273, 0.5),  # Ramain Aviv gimel
    GeoFilter(32.094103, 34.792462, 0.7),  # Yehuda Hamakabi
    # Herzliya
    GeoFilter(32.155013, 34.838615, 0.5),  # Neve Amirim
    GeoFilter(32.153692, 34.842297, 0.5),  # Ben Gurion Road South
    GeoFilter(32.157201, 34.842492, 0.3),  # Ben Gurion Road North



]