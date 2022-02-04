from enum import Enum


class Credentials(Enum):
    API_URL = 'https://api-lime-finance.affise.com/'
    API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
    LIMIT = 10000


class ConversionStatus(Enum):
    CONFIRMED = 1
    PENDING = 2
    DECLINED = 3
    HOLD = 5
    ALL = [1, 2, 3]


class ReportType(Enum):
    CONVERSIONS = '3.0/stats/conversions'
    CLICKS = '3.0/stats/clicks'


class PartnerID(Enum):
    LeadsTech = 3
    Leadgid = 30
    LeadsSU = 29
    Guruleads = 34
