from enum import Enum


class OfferId(Enum):
    lime = 7
    konga = 8
    mango = 9


class ConversionStatus(Enum):
    confirmed = 1
    pending = 2
    declined = 3
    not_found = 4
    hold = 5
