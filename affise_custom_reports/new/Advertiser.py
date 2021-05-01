import requests
import pandas as pd
from enum import Enum


class AdvId(Enum):
    LIME = '5a558391c3ebae42008b4567'
    KONGA = '5a558967c3ebae43008b4567'


class ConversionStatus(Enum):
    CONFIRMED = 1
    PENDING = 2
    DECLINED = 3
    NOT_FOUND = 4
    HOLD = 5
    ALL = [CONFIRMED, PENDING, DECLINED, NOT_FOUND, HOLD]


class ApiHeaders(Enum):
    API_URL = 'https://api-lime-finance.affise.com/'
    API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
    LIMIT = 2000


class Advertiser:

    def __init__(self, adv_id):
        self.adv_id = adv_id

    def single_api_request(self, date_from: str, date_to: str, status: list, advertiser: int, page: int, limit: int):
        response = requests.get(ApiHeaders.API_URL + '3.0/stats/conversions', headers={'API-Key': ApiHeaders.API_KEY},
                                params=('date_from': ))
