import requests
from datetime import datetime
import pandas as pd

api_url = 'https://api-lime-finance.affise.com/'
api_key = '1ad6cf31c5fbcfb05cf7be2529d6d5cb'


def get_aggregated_affiliate_stats(*, offer_id: int, date_from: str, date_to: str):
    conv_list = _create_conversion_list(offer_id=offer_id, date_from=date_from, date_to=date_to)
    conv_data_table = _create_conversion_data_table(conv_list)
    conv_data_frame = _create_data_frame(data=conv_data_table,
                                        columns=['partner_id', 'partner_name', 'goal_name', 'goal_value',
                                                 'action_id', 'click_id', 'date', 'sub1', 'sub2', 'sub3'])

    clicks_list = _create_clicks_list(offer_id=offer_id, date_from=date_from, date_to=date_to,
                                     slice=['year', 'month', 'day', 'affiliate'])
    clicks_data_table = _create_clicks_data_table(clicks_list)
    clicks_data_frame = _create_data_frame(data=clicks_data_table,
                                          columns=['date', 'affiliate', 'raw_clicks', 'uniq_clicks', 'conversions'])

    clicks_data = clicks_data_frame.groupby(by='affiliate').sum()
    clicks_data = clicks_data[clicks_data['conversions'] != 0]

    pivot_table = pd.pivot_table(conv_data_frame, index='partner_name', columns='goal_name',
                                 aggfunc='count', values='goal_value', fill_value=0, margins=False)

    cost = conv_data_frame[['partner_name', 'goal_value']]
    cost = cost.groupby(by=['partner_name']).sum()

    pivot_table['cost'] = cost['goal_value']
    pivot_table['conversions'] = clicks_data['conversions']
    pivot_table['raw_clicks'] = clicks_data['raw_clicks']
    pivot_table['uniq_clicks'] = clicks_data['uniq_clicks']
    pivot_table['total_loans'] = pivot_table['Займ хороший'] + pivot_table['Займ средний']

    pivot_table.rename(columns={
        'регистрация': 'regs',
    }, inplace=True)

    return pivot_table


def _get_conversions_api_request(*, offer_id: int, date_from: str, date_to: str, limit=5000, page=1):
    response = requests.get(api_url + '3.0/stats/conversions', headers={'API-Key': api_key},
                            params=(
                                ('date_from', date_from),
                                ('date_to', date_to),
                                ('offer', offer_id),
                                ('limit', limit),
                                ('page', page)
                            )).json()
    return response


def _get_custom_api_request(*, offer_id: int, slice: list, date_from: str, date_to: str, limit=500, page=1):
    response = requests.get(api_url + '3.0/stats/custom', headers={'API-Key': api_key},
                            params=(
                                ('slice[]', slice),
                                ('filter[date_from]', date_from),
                                ('filter[date_to]', date_to),
                                ('filter[offer]', offer_id),
                                ('limit', limit),
                                ('page', page)
                            )).json()
    return response


def _create_conversion_list(*, offer_id: int, date_from: str, date_to: str):
    api_response = _get_conversions_api_request(offer_id=offer_id, date_from=date_from, date_to=date_to, limit=1, page=1)
    pages = _count_pages(api_response=api_response, limit=5000)
    conversion_list = []
    for page in range(pages):
        r = _get_conversions_api_request(offer_id=offer_id, date_from=date_from, date_to=date_to, page=page + 1)
        for conversion in r['conversions']:
            conversion_list.append(conversion)

    return conversion_list


def _create_clicks_list(*, offer_id: int, slice: list, date_from: str, date_to: str):
    api_response = _get_custom_api_request(offer_id=offer_id, slice=slice, date_from=date_from, date_to=date_to, limit=1,
                                          page=1)
    pages = _count_pages(api_response=api_response, limit=500)
    clicks_list = []
    for page in range(pages):
        r = _get_custom_api_request(offer_id=offer_id, slice=slice, date_from=date_from, date_to=date_to, page=page + 1)
        for item in r['stats']:
            clicks_list.append(item)
    return clicks_list


def _create_conversion_data_table(conversion_list):
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


def _create_clicks_data_table(clicks_list):
    data_table = []
    for item in clicks_list:

        day = item.get('slice').get('day')
        month = item.get('slice').get('month')
        year = item.get('slice').get('year')
        date = str(datetime(year=year, month=month, day=day)).split(' ')[0]

        clicks_raw = int(item.get('traffic').get('raw'))
        clicks_uniq = int(item.get('traffic').get('uniq'))
        actions = int(item.get('actions').get('total').get('count'))

        if item.get('slice').get('affiliate') is not None:
            affiliate = item.get('slice').get('affiliate').get('name')

            data_table.append([date, affiliate, clicks_raw, clicks_uniq, actions])

    return data_table


def _count_pages(*, api_response, limit):
    pages = api_response['pagination']['total_count'] // limit + 1
    return pages


def _create_data_frame(*, data, columns):
    data_frame = pd.DataFrame(data=data, columns=columns)
    return data_frame
