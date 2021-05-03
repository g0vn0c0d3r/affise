from enum import Enum


class Credentials(Enum):
    API_URL = 'https://api-lime-finance.affise.com/'
    API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
    LIMIT = 5000


class ConversionStatus(Enum):
    CONFIRMED = 1
    PENDING = 2
    DECLINED = 3
    HOLD = 5
    ALL = [1, 2, 3]
