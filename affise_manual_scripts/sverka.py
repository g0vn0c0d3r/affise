import requests as r
import pandas as pd

API_URL = 'https://api-lime-finance.affise.com/'
API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'

date_from = '2022-02-01'
date_to = '2022-02-20'
status = 1
limit = 2000

resp = r.get(API_URL + '3.0/stats/conversions', headers={'API-Key': API_KEY},
             params=(
                 ('date_from', date_from),
                 ('date_to', date_to),
                 ('status', status),
                 ('limit', limit))
             ).json()

pages = resp['pagination']['total_count'] // resp['pagination']['per_page'] + 1

conversion_list = []
for page in range(pages):
    resp = r.get(API_URL + '3.0/stats/conversions', headers={'API-Key': API_KEY},
                 params=(
                     ('date_from', date_from),
                     ('date_to', date_to),
                     ('status', status),
                     ('limit', limit),
                     ('page', page + 1)
                 )).json()
    for conversions in resp['conversions']:
        conversion_list.append(conversions)

data = []
columns = ['ts', 'project', 'offer_title', 'goal_id', 'payouts',
           'sub1', 'sub2', 'sub3', 'affiliate']
for conversion in conversion_list:
    ts = conversion['created_at']
    project = conversion['advertiser']['title']
    offer_title = conversion['offer']['title']
    goal_id = conversion['action_id']
    payouts = conversion['payouts']
    sub1 = conversion['sub1']
    sub2 = conversion['sub2']
    sub3 = conversion['sub3']

    affiliate = conversion['partner']['title']

    data.append([ts, project, offer_title, goal_id, payouts, sub1, sub2, sub3, affiliate])

data_frame = pd.DataFrame(data=data, columns=columns)

aff_list = data_frame['affiliate'].unique()

for aff in aff_list:
    filtered_data = data_frame.query('affiliate == @aff').reset_index(drop=True)
    filtered_data.to_csv(f'reports/2022/february/{aff}.csv')
