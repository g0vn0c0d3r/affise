import requests
import pandas as pd
import datetime

API_URL = 'https://api-lime-finance.affise.com'
API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
LIMIT = 5000
LIME = '5a558391c3ebae42008b4567'
KONGA = '5a558967c3ebae43008b4567'


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


def get_conversions_df(advertiser: str, aff: str, web: str, date_from: str, date_to: str):

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

    conversions_dataframe = pd.DataFrame(data=conversions_list, columns=columns)

    conversions_dataframe.loc[conversions_dataframe['goal'] == 'регистрация', 'goal'] = 'registration'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Займ средний', 'goal'] = 'min_score_new_loan'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Займ хороший', 'goal'] = 'med_score_new_loan'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Займ отличный', 'goal'] = 'max_score_new_loan'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Повторный займ', 'goal'] = 'repeated_loan'

    conversions_dataframe['loan_category'] = conversions_dataframe.apply(goal_categorization, axis=1)

    if web == '0':
        if aff != '0':
            conversions_dataframe = conversions_dataframe.query('partner_id == @aff')
        else:
            pass
    else:
        conversions_dataframe = conversions_dataframe.query('partner_id == @aff and sub3 == @web')

    conversions_dataframe['date'] = pd.to_datetime(conversions_dataframe['date'])
    conversions_dataframe['week'] = conversions_dataframe['date'].dt.isocalendar().week
    conversions_dataframe['month'] = conversions_dataframe['date'].dt.month
    conversions_dataframe['year'] = conversions_dataframe['date'].dt.year

    return conversions_dataframe


def get_clicks_data(advertiser: str, aff: str, web: str, date_from: str, date_to: str):

    if web == '0':
        if aff != '0':
            clicks = requests.get(url=API_URL + '/3.0/stats/custom', headers={'API-Key': API_KEY},
                                  params=(
                                      ('slice[]', 'year'),
                                      ('slice[]', 'month'),
                                      ('slice[]', 'day'),
                                      ('filter[date_from]', date_from),
                                      ('filter[date_to]', date_to),
                                      ('filter[advertiser]', advertiser),
                                      ('filter[partner]', aff)
                                  )).json()
        else:
            clicks = requests.get(url=API_URL + '/3.0/stats/custom', headers={'API-Key': API_KEY},
                                  params=(
                                      ('slice[]', 'year'),
                                      ('slice[]', 'month'),
                                      ('slice[]', 'day'),
                                      ('filter[date_from]', date_from),
                                      ('filter[date_to]', date_to),
                                      ('filter[advertiser]', advertiser)
                                  )).json()
    else:
        clicks = requests.get(url=API_URL + '/3.0/stats/custom', headers={'API-Key': API_KEY},
                              params=(
                                  ('slice[]', 'year'),
                                  ('slice[]', 'month'),
                                  ('slice[]', 'day'),
                                  ('filter[date_from]', date_from),
                                  ('filter[date_to]', date_to),
                                  ('filter[advertiser]', advertiser),
                                  ('filter[partner]', aff),
                                  ('filter[sub3]', web)
                              )).json()

    clicks_list = []
    columns = ['date', 'clicks']

    for item in clicks['stats']:
        date = f'{item["slice"]["year"]}-{item["slice"]["month"]}-{item["slice"]["day"]}'
        clicks = int(item['traffic']['uniq'])

        clicks_list.append([date, clicks])

    df_clicks = pd.DataFrame(data=clicks_list, columns=columns)

    df_clicks['date'] = pd.to_datetime(df_clicks['date'])
    df_clicks['week'] = df_clicks['date'].dt.isocalendar().week
    df_clicks['month'] = df_clicks['date'].dt.month
    df_clicks['year'] = df_clicks['date'].dt.year

    return df_clicks


def get_dynamic_report(advertiser: str, aff: str, web: str, date_from: str, date_to: str, index: str):
    conversions = get_conversions_df(advertiser=advertiser, aff=aff, web=web, date_from=date_from, date_to=date_to)

    pivoted_conversions = conversions.pivot_table(index=index, columns='loan_category',
                                                  values='goal', aggfunc='count', fill_value=0)

    pivoted_conversions = pivoted_conversions[['reg', 'new', 'rep']]

    pivoted_budget = conversions.pivot_table(index=index, columns='loan_category',
                                             values='payouts', aggfunc='sum', fill_value=0)

    pivoted_budget.drop(columns=['reg'], inplace=True)

    pivoted_budget.rename(columns={'new': 'costs_new', 'rep': 'costs_rep'}, inplace=True)

    pivoted_budget['costs_total'] = pivoted_budget['costs_new'] + pivoted_budget['costs_rep']

    conversions_final_df = pd.merge(pivoted_conversions, pivoted_budget, how='left', left_index=True, right_index=True)

    clicks = get_clicks_data(advertiser=advertiser, aff=aff, web=web, date_from=date_from, date_to=date_to)
    clicks = clicks.groupby(by=index).agg({'clicks': 'sum'})

    merged_data = pd.merge(clicks, conversions_final_df, how='left', left_index=True, right_index=True)

    merged_data['CR%'] = ((merged_data['reg'] / merged_data['clicks']) * 100).round(1)
    merged_data['AR%'] = ((merged_data['new'] / merged_data['reg']) * 100).round(1)
    merged_data['RLS%'] = ((merged_data['rep'] / (merged_data['new'] + merged_data['rep'])) * 100).round(1)
    merged_data['EPC'] = (merged_data['costs_total'] / merged_data['clicks']).astype(int)
    merged_data['CPAn'] = (merged_data['costs_new'] / merged_data['new']).astype(int)
    merged_data['CPAr'] = (merged_data['costs_total'] / merged_data['new']).astype(int)

    return merged_data