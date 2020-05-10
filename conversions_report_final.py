import requests
import pandas as pd
import numpy as np

api_url = 'https://api-lime-finance.affise.com/'
api_key = '1ad6cf31c5fbcfb05cf7be2529d6d5cb'

start_date = '2020-01-01'
end_date = '2020-04-30'
page_limit = 5000


def get_sverka():
    get_raw_data()
    get_pages()
    create_data_table()
    create_pivot_table()
    pass


def get_raw_data(
        *,
        date_from: str,
        date_to: str,
        offer_id: int,
        conversions_status: int,
        conversions_per_page: int,
        page: int):

    r = requests.get(
        api_url + '3.0/stats/conversions',
        headers={'API-Key': api_key},
        params=(
            ('date_from', date_from),
            ('date_to', date_to),
            ('offer', offer_id),
            ('status', conversions_status),
            ('limit', conversions_per_page),
            ('page', page),
            )
        ).json()

    return r


def get_pages(api_response):
    pages = api_response['pagination']['total_count'] // page_limit + 1
    return pages


response = get_raw_data(date_from=start_date, date_to=end_date, offer_id=7, conversions_status=1, conversions_per_page=page_limit, page=1)

pages = count_pages(response)
print(pages)

# monthly_data = get_raw_data(date_from=start, date_to=stop, offer=7, status=1, limit=5000, page=1)
#
# data_table = []
# for item in range(len(monthly_data['conversions'])):
#     partner_id = monthly_data['conversions'][item]['partner_id']
#     partner_name = monthly_data['conversions'][item]['partner']['name']
#     goal_name = monthly_data['conversions'][item]['goal']
#     goal_value = round(monthly_data['conversions'][item]['revenue'])
#     conversion_id = monthly_data['conversions'][item]['conversion_id']
#     click_id = monthly_data['conversions'][item]['clickid']
#     created_at = monthly_data['conversions'][item]['created_at']
#     webmaster_id = monthly_data['conversions'][item]['sub3']
#
#     data_table.append([
#         partner_id,
#         partner_name,
#         goal_name,
#         goal_value,
#         conversion_id,
#         click_id,
#         created_at,
#         webmaster_id
#
#     ])
#
#
# df = pd.DataFrame(data=data_table,
#                   columns=[
#                       'partner_id',
#                       'partner_name',
#                       'goal_name',
#                       'goal_value',
#                       'conversion_id',
#                       'click_id',
#                       'created_at',
#                       'webmaster_id'])
# sample = df.head(30)
# print(sample)
#
# table = pd.pivot_table(df, index='partner_id', columns='goal_name', values='goal_value', aggfunc='count', fill_value=0, margins=True)
# table.sort_values(by='All', ascending=False, inplace=True)
# print(table)
