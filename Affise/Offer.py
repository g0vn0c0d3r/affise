import requests
from Affise.Constants import ConversionStatus


class Offer:
    __page_limit = 5000
    __api_url = 'https://api-lime-finance.affise.com/'
    __api_key = '1ad6cf31c5fbcfb05cf7be2529d6d5cb'

    def __init__(self, offer_id):
        self.offer_id = offer_id

    def get_sverka(self, date_from, date_to, status=ConversionStatus.confirmed.value):
        response = self.api_conversions_request(
            date_from=date_from,
            date_to=date_to,
            status=status
        )

        pages = response['pagination']['total_count'] // self.__page_limit + 1

        conversion_list = []
        for page in range(pages):
            r = self.api_conversions_request(
                date_from=date_from,
                date_to=date_to,
                status=ConversionStatus.confirmed.value,
                page=page+1
            )
            for conversion in r['conversions']:
                conversion_list.append(conversion)
        return len(conversion_list), conversion_list

    def api_conversions_request(self, date_from: str, date_to: str, status: int, limit=__page_limit, page=1):
        response = requests.get(
            self.__api_url + '3.0/stats/conversions',
            headers={'API-Key': self.__api_key},
            params=(
                ('date_from', date_from),
                ('date_to', date_to),
                ('offer', self.offer_id),
                ('status', status),
                ('limit', limit),
                ('page', page))
            ).json()
        return response

    def create_conversion_list(self, pages, date_from, date_to, status=ConversionStatus.confirmed.value):
        conversion_list = []
        for page in range(pages):
            r = self.api_conversions_request(date_from=date_from, date_to=date_to, status=status, page=page+1)
            for conversion in r['conversions']:
                conversion_list.append(conversion)

        return len(conversion_list), conversion_list

