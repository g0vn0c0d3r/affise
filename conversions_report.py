import requests

api_url = 'https://api-lime-finance.affise.com/'
api_key = 'c666e444eabc1706574ec7973ae4e677'


def get_raw_data(*, date_from, date_to, offer, limit, page):
    r = requests.get(
        api_url + '3.0/stats/conversions',
        headers={'API-Key': api_key},
        params=(
            ('date_from', date_from),
            ('date_to', date_to),
            ('offer', offer),
            ('limit', limit),
            ('page', page),
        )
    ).json()

    return r


pages = get_raw_data(
    date_from='2020-02-15',
    date_to='2020-03-14',
    offer=15,
    limit=1,
    page=1)['pagination']['total_count'] // 1000 + 1


conversions_list = []
for page in range(pages):
    req = get_raw_data(date_from='2020-02-15', date_to='2020-03-14', offer=15, limit=1000, page=(page + 1))
    # print(len(req['conversions']))
    for conversion in req['conversions']:
        affiliate = conversion['partner']['id']
        webmaster = int(conversion['sub3']) if conversion['sub3'].isdigit() == True

        payload = {
            'affiliate': affiliate,
            'webmaster': if conversion['sub3'].isdigit() == True: conversion['sub3']

        }
        print(payload)



# lst = []
#
# for i in range(len(conversions_data['conversions'])):
#     data = conversions_data['conversions'][i]
#
#     payload = {
#         'affiliate': data['partner']['id'],
#         'webmaster': int(data['sub3']),
#         'registrations': 1 if data['goal_value'] == '1' else 0,
#         'loans': 1 if data['goal_value'] == '2' else 0,
#         'revenue': data['revenue']
#     }
#     lst.append(payload)
#
# # print()
#
# lst = sorted(lst, key=lambda x: x['webmaster'])
# # for i in lst:
# #     print(i)
#
# new_list = []
# for i in range(len(lst)):
#     payload = {
#         'affiliate': lst[i].get('affiliate'),
#         'webmaster': lst[i].get('webmaster'),
#         'registrations': 0,
#         'loans': 0,
#         'revenue': 0
#     }
#     if payload not in new_list:
#         new_list.append(payload)
# # print()
# # for i in new_list:
# #     print(i)
#
#
# for i in range(len(lst)):
#     for j in range(len(new_list)):
#         if lst[i].get('affiliate') == new_list[j].get('affiliate') and lst[i].get('webmaster') == new_list[j].get('webmaster'):
#             new_list[j]['registrations'] += lst[i]['registrations']
#             new_list[j]['loans'] += lst[i]['loans']
#             new_list[j]['revenue'] += lst[i]['revenue']
#
# for i in sorted(new_list, key=lambda x: x['revenue'], reverse=True):
#     print(i)
