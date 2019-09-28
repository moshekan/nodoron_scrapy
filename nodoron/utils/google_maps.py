from functools import lru_cache
import googlemaps
import datetime as dt
import os


@lru_cache()
def get_gmaps_client() -> googlemaps.Client:
    return googlemaps.Client(key=os.environ.get('GOOGLE_MAPS_API_KEY'))


@lru_cache()
def get_transit_routes(origin: str, destination: str, time: dt.datetime) -> list:
    client = get_gmaps_client()
    return client.directions(origin=origin, destination=destination, departure_time=time, mode='transit')


def is_reachable_by_one_bus(origin: str, destination: str, time: dt.datetime) -> bool:
    routes = get_transit_routes(origin, destination, time)
    for route in routes:
        steps = route['legs'][0]['steps']
        if sum([1 for step in steps if step['travel_mode'] == 'TRANSIT']) == 1:
            return True

    return False


def get_min_number_of_busses(origin: str, destination: str, time: dt.datetime) -> int:
    num_of_busses_list = []
    routes = get_transit_routes(origin, destination, time)
    for route in routes:
        steps = route['legs'][0]['steps']
        num_of_busses_list.append(sum([1 for step in steps if step['travel_mode'] == 'TRANSIT']))

    return min(num_of_busses_list, default=0)
