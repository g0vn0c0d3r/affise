import requests
import pandas as pd
import datetime

API_URL = 'https://api-lime-finance.affise.com'
API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
LIMIT = 5000
LIME_ADV_ID = '5a558391c3ebae42008b4567'
KONGA_ADV_ID = '5a558967c3ebae43008b4567'


def goal_categorization(row):
    goal = row['goal']

    if goal == 'registration':
        return 'reg'
    elif goal == 'repeated_loan':
        return 'rep'
    else:
        return 'new'


def single_api_conv_request(advertiser: str, date_from: str, date_to: str, page=1, limit=1):
    resp = requests.get(url=API_URL + '/3.0/stats/conversions', headers={'API-Key': API_KEY},
                        params=(('date_from', date_from),
                                ('date_to', date_to),
                                ('advertiser', advertiser),
                                ('page', page),
                                ('limit', limit))
                        )
    return resp.json()


def get_conv_raw_data(advertiser: str, date_from: str, date_to: str, groupby: str):
    pages = single_api_conv_request(
        advertiser=advertiser,
        date_from=date_from,
        date_to=date_to)['pagination']['total_count'] // LIMIT + 1

    raw_conversions = []
    for page in range(pages):
        conversions = single_api_conv_request(date_from=date_from,
                                              date_to=date_to,
                                              advertiser=advertiser,
                                              page=page + 1,
                                              limit=LIMIT)['conversions']

        raw_conversions.extend(conversions)

    conversions_list = []
    columns = ['date', 'action_id', 'click_id', 'status', 'offer_id', 'goal', 'payouts',
               'partner', 'partner_id', 'referrer', 'sub1', 'sub2', 'sub3']

    for conversion in raw_conversions:
        date = conversion['created_at'].split(' ')[0]
        action_id = conversion['action_id']
        click_id = conversion['clickid']
        status = conversion['status']
        offer_id = conversion['offer_id']
        goal = conversion['goal']
        payouts = conversion['payouts']
        partner = conversion['partner']['name']
        partner_id = str(conversion['partner']['id'])
        referrer = conversion['referrer']
        sub1 = conversion['sub1']
        sub2 = conversion['sub2']
        sub3 = conversion['sub3']

        conversions_list.append([date, action_id, click_id, status, offer_id, goal, payouts,
                                 partner, partner_id, referrer, sub1, sub2, sub3])

    df_conv = pd.DataFrame(data=conversions_list, columns=columns)

    df_conv.loc[df_conv['goal'] == 'регистрация', 'goal'] = 'registration'
    df_conv.loc[df_conv['goal'] == 'Займ средний', 'goal'] = 'min_score_new_loan'
    df_conv.loc[df_conv['goal'] == 'Займ хороший', 'goal'] = 'med_score_new_loan'
    df_conv.loc[df_conv['goal'] == 'Займ отличный', 'goal'] = 'max_score_new_loan'
    df_conv.loc[df_conv['goal'] == 'Повторный займ', 'goal'] = 'repeated_loan'

    df_conv['loan_category'] = df_conv.apply(goal_categorization, axis=1)

    pivoted_conversions = df_conv.pivot_table(index=groupby, columns='loan_category', values='goal',
                                              aggfunc='count', fill_value=0).reset_index()
    pivoted_conversions['date'] = pd.to_datetime(pivoted_conversions['date'])

    clicks = requests.get(url=API_URL + '/3.0/stats/custom', headers={'API-Key': API_KEY},
                          params=(
                              ('slice[]', 'year'),
                              ('slice[]', 'month'),
                              ('slice[]', 'day'),
                              ('filter[date_from]', date_from),
                              ('filter[date_to]', date_to)
                          )).json()

    clicks_list = []
    columns = ['date', 'clicks']
    for item in clicks['stats']:
        date = f'{item["slice"]["year"]}-{item["slice"]["month"]}-{item["slice"]["day"]}'
        clicks = int(item['traffic']['uniq'])

        clicks_list.append([date, clicks])

    df_clicks = pd.DataFrame(data=clicks_list, columns=columns)
    df_clicks['date'] = pd.to_datetime(df_clicks['date'])

    output_data = pd.merge(df_clicks, pivoted_conversions, on='date')

    output_data['CR%'] = ((output_data['reg'] / output_data['clicks']) * 100).round(2)

    return output_data
