import requests
from Affise.Constants import ConversionStatus
import pandas as pd


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
            status=status,
            limit=1
        )

        pages = response['pagination']['total_count'] // self.__page_limit + 1

        conversion_list = self.create_conversion_list(pages=pages, date_from=date_from, date_to=date_to, status=status)

        data_table = self.create_data_table(conversion_list)
        data_frame = self.create_data_frame(data_table)
        pivot_table = self.create_pivot_table(data_frame,
                                              index=['partner_id', 'partner_name'],
                                              columns='goal_name',
                                              values='goal_value',
                                              aggfunc='count',
                                              fill_value=0,
                                              margins=True
                                              )
        return pivot_table

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

    def create_conversion_list(self, pages, date_from, date_to, status):
        conversion_list = []
        for page in range(pages):
            r = self.api_conversions_request(date_from=date_from, date_to=date_to, status=status, page=page+1)
            for conversion in r['conversions']:
                conversion_list.append(conversion)

        return conversion_list

    @staticmethod
    def create_data_table(conversion_list):
        data_table = []
        for conversion in conversion_list:
                partner_id = conversion['partner_id']
                partner_name = conversion['partner']['name']
                goal_name = conversion['goal']
                goal_value = round(conversion['revenue'])
                conversion_id = conversion['conversion_id']
                click_id = conversion['clickid']
                created_at = conversion['created_at']
                webmaster_id = conversion['sub3']

                data_table.append([
                    partner_id,
                    partner_name,
                    goal_name,
                    goal_value,
                    conversion_id,
                    click_id,
                    created_at,
                    webmaster_id
                ])
        return data_table

    @staticmethod
    def create_data_frame(data_table):
        data_frame = pd.DataFrame(data=data_table,
                                  columns=[
                                      'partner_id',
                                      'partner_name',
                                      'goal_name',
                                      'goal_value',
                                      'conversion_id',
                                      'click_id',
                                      'created_at',
                                      'webmaster_id']
                                  )
        return data_frame

    @staticmethod
    def create_pivot_table(data_frame, *, index, columns, values, aggfunc, fill_value, margins):
        pivot_table = pd.pivot_table(data_frame, index=index, columns=columns, values=values,
                                     aggfunc=aggfunc, fill_value=fill_value, margins=margins)
        return pivot_table






















