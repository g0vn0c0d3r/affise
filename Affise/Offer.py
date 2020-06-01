import requests
from Affise.Constants import ConversionStatus
from Affise.Constants import OfferId
import pandas as pd


class Offer:
    __page_limit = 5000
    __api_url = 'https://api-lime-finance.affise.com/'
    __api_key = '1ad6cf31c5fbcfb05cf7be2529d6d5cb'

    def __init__(self, offer_id):
        self.offer_id = offer_id

    # DONE
    def get_aggregated_monthly_stats(self, *, date_from: str, date_to: str, status=ConversionStatus.confirmed.value):
        pages = self._count_pages(date_from=date_from, date_to=date_to, status=status)
        conversion_list = self._create_conversion_list(pages=pages, date_from=date_from, date_to=date_to, status=status)
        data_table = self._create_data_table(conversion_list)
        data_frame = self._create_data_frame(data_table)
        pivot_table = self._create_pivot_table(data_frame, index='partner_name', columns='goal_name',
                                               values='goal_value', aggfunc='count', fill_value=0, margins=True)
        pivot_table.sort_values(by=['All'], axis=0, ascending=False, inplace=True)
        return pivot_table

    # DONE
    def get_partners_daily_stats(self, *, date_from: str, date_to: str, status=ConversionStatus.confirmed.value):
        pages = self._count_pages(date_from=date_from, date_to=date_to, status=status)
        conversion_list = self._create_conversion_list(pages=pages, date_from=date_from, date_to=date_to, status=status)
        data_table = self._create_data_table(conversion_list)
        data_frame = self._create_data_frame(data_table)
        pivot_table = self._create_pivot_table(data_frame, index='date', columns='partner_name', aggfunc='count',
                                               values='goal_value', margins=True, fill_value=0)
        pivot_table.sort_values(by=['All'], axis=1, ascending=False, inplace=True)

        return pivot_table

    # DONE
    def get_daily_stats(self, *, date_from: str, date_to: str, status=ConversionStatus.confirmed.value):
        pages = self._count_pages(date_from=date_from, date_to=date_to, status=status)
        conversion_list = self._create_conversion_list(pages=pages, date_from=date_from, date_to=date_to, status=status)
        data_table = self._create_data_table(conversion_list)
        data_frame = self._create_data_frame(data_table)
        pivot_table = self._create_pivot_table(data_frame, index='date', columns='goal_name', aggfunc='count',
                                               values='goal_value', margins=True, fill_value=0)
        pivot_table.sort_values(by=['All'], axis=0, ascending=False, inplace=True)

        return pivot_table

    # DONE
    def get_csv_reports(self, *, date_from: str, date_to: str, path: str, status=ConversionStatus.confirmed.value):
        pages = self._count_pages(date_from=date_from, date_to=date_to, status=status)
        conversion_list = self._create_conversion_list(pages=pages, date_from=date_from, date_to=date_to, status=status)
        unique_partner_list = sorted(self._get_unique_partner_list(conversion_list))
        data_table = self._create_data_table(conversion_list)
        data_frame = self._create_data_frame(data_table)

        for partner in unique_partner_list:
            unique_partner_report = data_frame[data_frame['partner_id'] == partner]
            unique_partner_report.reset_index(drop=True, inplace=True)
            unique_partner_report.to_csv(
                path + str(str(f'{OfferId(self.offer_id).name}') + '_' + 'pid_' + f'{partner}') + '_' + str(
                    f'{date_from}') + '_' + str(f'{date_to}' + '.csv'))

    def _api_conversions_request(self, date_from: str, date_to: str, status: int, limit=__page_limit, page=1):
        response = requests.get(self.__api_url + '3.0/stats/conversions', headers={'API-Key': self.__api_key},
                                params=(
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('offer', self.offer_id),
                                    ('status', status),
                                    ('limit', limit),
                                    ('page', page)
                                )).json()
        return response

    def _count_pages(self, date_from, date_to, status):

        response = self._api_conversions_request(
            date_from=date_from,
            date_to=date_to,
            status=status,
            limit=1
        )

        pages = response['pagination']['total_count'] // self.__page_limit + 1
        return pages

    def _create_conversion_list(self, pages, date_from, date_to, status):
        conversion_list = []
        for page in range(pages):
            r = self._api_conversions_request(date_from=date_from, date_to=date_to, status=status, page=page + 1)
            for conversion in r['conversions']:
                conversion_list.append(conversion)

        return conversion_list

    @staticmethod
    def _create_data_table(conversion_list):
        data_table = []
        for conversion in conversion_list:
            partner_id = conversion['partner_id']
            partner_name = conversion['partner']['name']
            goal_name = conversion['goal']
            goal_value = round(conversion['revenue'])
            action_id = conversion['action_id']
            click_id = conversion['clickid']
            date = conversion['created_at'].split(' ')[0]
            sub1 = conversion['sub1']
            sub2 = conversion['sub2']
            sub3 = conversion['sub3']

            data_table.append([
                partner_id,
                partner_name,
                goal_name,
                goal_value,
                action_id,
                click_id,
                date,
                sub1,
                sub2,
                sub3
            ])
        return data_table

    @staticmethod
    def _create_data_frame(data_table):
        data_frame = pd.DataFrame(data=data_table,
                                  columns=[
                                      'partner_id',
                                      'partner_name',
                                      'goal_name',
                                      'goal_value',
                                      'action_id',
                                      'click_id',
                                      'date',
                                      'sub1',
                                      'sub2',
                                      'sub3'
                                  ]
                                  )
        return data_frame

    @staticmethod
    def _create_pivot_table(data_frame, *, index, columns, values, aggfunc, fill_value, margins):
        pivot_table = pd.pivot_table(data_frame, index=index, columns=columns, values=values,
                                     aggfunc=aggfunc, fill_value=fill_value, margins=margins)
        return pivot_table

    @staticmethod
    def _get_unique_partner_list(conversion_list):
        unique_partner_list = []
        for conversion in conversion_list:
            partner_id = conversion['partner']['id']
            if partner_id not in unique_partner_list:
                unique_partner_list.append(partner_id)
        return unique_partner_list
