from .utils.yad2_api import Yad2ApiRealEstateWrapper, Range, City
from .utils.geo_filters import GeoFilter

SEARCH_URLS = [
    Yad2ApiRealEstateWrapper(rooms=Range(4, 6), price=Range(0, 7500), city=City.TEL_AVIV),
    Yad2ApiRealEstateWrapper(rooms=Range(4, 6), price=Range(0, 7500), city=City.HERZLIYA),
]

GEO_FILTERS = [
    # Tel aviv
    GeoFilter(32.103963, 34.803351, 1),  # Tel Aviv University Train Station
    GeoFilter(32.108510, 34.792238, 1.5),  # Ramat Aviv Alef
    GeoFilter(32.116657, 34.794643, 1.8),  # Neve Avivim
    GeoFilter(32.123046, 34.798273, 1.5),  # Ramat Aviv gimel
    GeoFilter(32.094103, 34.792462, 1),  # Yehuda Hamakabi
    # Herzliya
    GeoFilter(32.155013, 34.838615, 0.5),  # Neve Amirim
    GeoFilter(32.153692, 34.842297, 0.8),  # Ben Gurion Road South
    # Ben Gurion Road North
    GeoFilter(32.157201, 34.842492, 0.5),
    GeoFilter(32.152358, 34.841837, 0.5),
    GeoFilter(32.153196, 34.842121, 0.7),
    GeoFilter(32.160099, 34.841955, 0.5),
    GeoFilter(32.162815, 34.842624, 0.5),




]