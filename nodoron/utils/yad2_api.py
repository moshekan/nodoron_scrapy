from enum import Enum
from typing import List

from requests import get


PHONE_API_URL = 'https://www.yad2.co.il/api/item/{item_id}/contactinfo?id={item_id}'

URL_BASE_FORMAT = 'https://www.yad2.co.il/api/feed/get?'
REAL_ESTATE_CATEGORY = 2
RENT_SUB_CATEGORY = 2


class City(Enum):
    TEL_AVIV = 5000
    HERZLIYA = 6400


class Neighborhood(Enum):
    TEL_AVIV_OLD_NORTH = 1483
    TEL_AVIV_NEVE_AVIVIM = 196
    TEL_AVIV_RAMAT_AVIV = 197
    TEL_AVIV_RAMAT_AVIV_GIMEL = 1515
    TEL_AVIV_UNIVERSITY = 846
    TEL_AVIV_TOHNIT_LAMED = 849
    TEL_AVIV_AFEKA = 1514
    TEL_AVIV_NEW_NORTH = 204
    TEL_AVIV_BAVLI = 1518
    TEL_AVIV_KIKAR_HAMEDINA = 1516


class Range:
    """
    Represents a range param in for the APIs request.
    For example Range(1, 5) will be '1-5'.
    """

    def __init__(self, range_min: int, range_max: int = None):
        self.range_min = range_min
        self.range_max = range_max

    def __str__(self):
        range_min = self.range_min if self.range_min else -1
        range_max = self.range_max if self.range_max else -1
        return f'{range_min}-{range_max}'


def get_yad2_search_url(price: Range, rooms: Range, city: City, neighborhood: Neighborhood = None) -> str:
    """
    Gets a url with which to search yad2 based on given self explained parameters
    """

    param_dict = {
        'cat': REAL_ESTATE_CATEGORY,
        'subcat': RENT_SUB_CATEGORY,
        'city': city.value,
        'price': str(price),
        'rooms': str(rooms),
        'page': 1,
    }
    if neighborhood:
        param_dict['neighborhood'] = neighborhood.value

    get_params = '&'.join([f'{key}={value}' for key, value in param_dict.items()])
    return URL_BASE_FORMAT + get_params


def get_phone_list(yad2_id: str) -> List[str]:
    """
    Get a list of phone numbers given a yad2 id
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like G'
                             'ecko) Chrome/75.0.3770.100 Safari/537.36'}
    response = get(PHONE_API_URL.format(yad2_id=yad2_id), headers=headers).json()
    phone_list = [phone['title'].replace('-', '') for phone in response['data']['phone_numbers']]
    return phone_list
