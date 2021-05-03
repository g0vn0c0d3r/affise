import requests
import pandas as pd
import Config


class Advertiser:

    def __init__(self, id):
        self.id = id

    def single_api_conversions_request(self, date_from: str, date_to: str, limit=1, page=1):

        response = requests.get(Config.Credentials.API_URL.value + '3.0/stats/conversions',
                                headers={'API-Key': Config.Credentials.API_KEY.value},
                                params=(
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('advertiser', self.id),
                                    ('limit', limit),
                                    ('page', page)
                                )).json()
        return response

    def create_conversions_list(self, date_from: str, date_to: str):
        pages = self.single_api_conversions_request(date_from=date_from, date_to=date_to)['pagination']['total_count'] // \
                Config.Credentials.LIMIT.value + 1

        conversion_list = []
        for page in range(pages):
            conversions = self.single_api_conversions_request(date_from=date_from,
                                                              date_to=date_to,
                                                              page=page + 1,
                                                              limit=Config.Credentials.LIMIT.value)['conversions']

            conversion_list.extend(conversions)
        return conversion_list, len(conversion_list)

