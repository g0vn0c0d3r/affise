import numpy as np
import requests
import pandas as pd


API_URL = 'https://api-lime-finance.affise.com'
API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
LIMIT = 2500
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


def single_api_conversions_request(advertiser: str, affiliate: str, web: str, date_from: str, date_to: str, page=1, limit=1):
    if web != '0':
        resp = requests.get(url=API_URL + '/3.0/stats/conversions', headers={'API-Key': API_KEY},
                            params=(
                                ('advertiser', advertiser),
                                ('partner[]', int(affiliate)),
                                ('subid3', web),
                                ('date_from', date_from),
                                ('date_to', date_to),
                                ('page', page),
                                ('limit', limit)))

    else:
        if affiliate == '0':
            resp = requests.get(url=API_URL + '/3.0/stats/conversions', headers={'API-Key': API_KEY},
                                params=(
                                    ('advertiser', advertiser),
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('page', page),
                                    ('limit', limit)))
        else:
            resp = requests.get(url=API_URL + '/3.0/stats/conversions', headers={'API-Key': API_KEY},
                                params=(
                                    ('advertiser', advertiser),
                                    ('partner[]', int(affiliate)),
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('page', page),
                                    ('limit', limit)))
    return resp.json()


def single_api_clicks_request(advertiser: str, affiliate: str, web: str, date_from: str, date_to: str, page=1, limit=3):
    if web != '0':
        response = requests.get(url=API_URL + '/3.0/stats/getbydate', headers={'API-Key': API_KEY},
                                params=(
                                    ('filter[date_from]', date_from),
                                    ('filter[date_to]', date_to),
                                    ('filter[advertiser]', advertiser),
                                    ('filter[partner]', affiliate),
                                    ('filter[sub3]', web),
                                    ('page', page),
                                    ('limit', limit)
                                )).json()

    else:
        if affiliate == '0':
            response = requests.get(url=API_URL + '/3.0/stats/getbydate', headers={'API-Key': API_KEY},
                                    params=(
                                      ('filter[date_from]', date_from),
                                      ('filter[date_to]', date_to),
                                      ('filter[advertiser]', advertiser),
                                      ('page', page),
                                      ('limit', limit)
                                  )).json()
        else:
            response = requests.get(url=API_URL + '/3.0/stats/getbydate', headers={'API-Key': API_KEY},
                                    params=(
                                        ('filter[date_from]', date_from),
                                        ('filter[date_to]', date_to),
                                        ('filter[advertiser]', advertiser),
                                        ('filter[partner]', affiliate),
                                        ('filter[sub3]', web),
                                        ('page', page),
                                        ('limit', limit)
                                    )).json()
    return response


def get_conversions_dataframe(advertiser: str, affiliate: str, web: str, date_from: str, date_to: str):
    pages = single_api_conversions_request(advertiser=advertiser, affiliate=affiliate, web=web,
                                           date_from=date_from, date_to=date_to)['pagination']['total_count'] // LIMIT + 1

    raw_conversions = []
    for page in range(pages):
        conversions = single_api_conversions_request(advertiser=advertiser, affiliate=affiliate, web=web,
                                                     date_from=date_from, date_to=date_to,
                                                     page=page+1, limit=LIMIT)['conversions']

        raw_conversions.extend(conversions)

    columns = ['date', 'action_id', 'click_id', 'status', 'offer_id', 'goal', 'payouts',
               'partner', 'partner_id', 'referrer', 'sub1', 'sub2', 'sub3']

    conversions_list = []
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

        conversions_list.append([date, action_id, click_id, status, offer_id, goal, payouts, partner, partner_id, referrer, sub1, sub2, sub3])

    conversions_dataframe = pd.DataFrame(data=conversions_list, columns=columns)

    conversions_dataframe.loc[conversions_dataframe['goal'] == 'регистрация', 'goal'] = 'registration'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Займ средний', 'goal'] = 'min_score_new_loan'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Займ хороший', 'goal'] = 'med_score_new_loan'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Займ отличный', 'goal'] = 'max_score_new_loan'
    conversions_dataframe.loc[conversions_dataframe['goal'] == 'Повторный займ', 'goal'] = 'repeated_loan'

    conversions_dataframe['loan_category'] = conversions_dataframe.apply(goal_categorization, axis=1)

    conversions_dataframe['date'] = pd.to_datetime(conversions_dataframe['date'])
    conversions_dataframe['week'] = conversions_dataframe['date'].dt.isocalendar().week
    conversions_dataframe['month'] = conversions_dataframe['date'].dt.month
    conversions_dataframe['year'] = conversions_dataframe['date'].dt.year

    return conversions_dataframe


def get_clicks_dataframe(advertiser: str, affiliate: str, web: str, date_from: str, date_to: str, limit=10):
    pages = single_api_clicks_request(advertiser=advertiser, affiliate=affiliate, web=web, date_from=date_from,
                                      date_to=date_to)['pagination']['total_count'] // limit + 1

    raw_clicks = []
    for page in range(pages):
        clicks = single_api_clicks_request(advertiser=advertiser, affiliate=affiliate, web=web,
                                           date_from=date_from, date_to=date_to,
                                           page=page+1, limit=limit)['stats']
        raw_clicks.extend(clicks)

    clicks_list = []
    columns = ['date', 'clicks']
    for item in raw_clicks:
        date = f'{item["slice"]["year"]}-{item["slice"]["month"]}-{item["slice"]["day"]}'
        clicks = int(item['traffic']['uniq'])

        clicks_list.append([date, clicks])

    df_clicks = pd.DataFrame(data=clicks_list, columns=columns).fillna(0)

    df_clicks['date'] = pd.to_datetime(df_clicks['date'])
    df_clicks['week'] = df_clicks['date'].dt.isocalendar().week
    df_clicks['month'] = df_clicks['date'].dt.month
    df_clicks['year'] = df_clicks['date'].dt.year

    return df_clicks


def get_dynamic_report(conv_df, clicks_df, index: str):
    pivoted_conversions = conv_df.pivot_table(index=index, columns='loan_category',
                                              values='goal', aggfunc='count', fill_value=0)
    # pivoted_conversions = pivoted_conversions[['reg', 'new', 'rep']]
    pivoted_conversions['total'] = pivoted_conversions['new'] + pivoted_conversions['rep']

    pivoted_budget = conv_df.groupby(by=index).sum()['payouts']

    conversions_data = pd.merge(pivoted_conversions, pivoted_budget, how='left', left_index=True, right_index=True)

    clicks_data = clicks_df.groupby(by=index).sum()['clicks'].to_frame()

    output_data = pd.merge(clicks_data, conversions_data, how='left', left_index=True, right_index=True)
    output_data.fillna(0, inplace=True)

    output_data['CR%'] = round((output_data['reg'] / output_data['clicks']) * 100, 1)
    output_data['AR%'] = round((output_data['new'] / output_data['reg']) * 100, 1)
    output_data['RLS%'] = round((output_data['rep'] / output_data['total']) * 100, 1)

    output_data['EPC'] = output_data['payouts'] / output_data['clicks']
    output_data['EPL'] = output_data['payouts'] / output_data['reg']
    output_data['CPAn'] = (output_data['payouts'] - output_data['rep'] * 500)/output_data['new']
    output_data['CPAr'] = output_data['payouts'] / output_data['new']


    # Меняем inf nan
    output_data.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Меняем nan на 0
    output_data.fillna(0, inplace=True)

    # Изменим типы данных для некоторых столбцов
    chng_cols = ['reg', 'new', 'rep', 'total', 'payouts', 'EPC', 'EPL', 'CPAn', 'CPAr']
    for col in chng_cols:
        output_data[col] = output_data[col].astype(int)

    output_data = output_data[['clicks', 'reg', 'new', 'rep', 'total', 'CR%', 'AR%',
                               'RLS%', 'payouts', 'EPC', 'EPL', 'CPAn', 'CPAr']]

    return output_data

# def get_conversion_pivot(advertiser: str, affiliate: str, web: str, date_from: str, date_to: str, index: str):
#     conversion_df = get_conversions_dataframe(advertiser=advertiser, affiliate=affiliate, web=web, date_from=date_from,
#                                               date_to=date_to)
#
#     pivoted_conversions = conversion_df.pivot_table(index=index, columns='loan_category',
#                                                     values='goal', aggfunc='count', fill_value=0)
#     pivoted_conversions = pivoted_conversions[['reg', 'new', 'rep']]
#     pivoted_conversions['total'] = pivoted_conversions['new'] + pivoted_conversions['rep']
#
#     pivoted_budget = conversion_df.groupby(by=index).sum()['payouts']
#
#     # pivoted_budget = conversion_df.pivot_table(index=index, columns='loan_category',
#     #                                            values='payouts', aggfunc='sum', fill_value=0)
#     # pivoted_budget.drop(columns=['reg'], inplace=True)
#     # pivoted_budget.rename(columns={'new': 'costs_new', 'rep': 'costs_rep'}, inplace=True)
#
#     merged_conversion_data = pd.merge(pivoted_conversions, pivoted_budget, how='left', left_index=True, right_index=True)
#
#     return merged_conversion_data

#
#
# def get_dynamic_report(advertiser: str, affiliate: str, web: str, date_from: str, date_to: str, index: str):
#     conversions = get_conversions_data(advertiser=advertiser, aff=aff, web=web, date_from=date_from, date_to=date_to)
#
#     pivoted_conversions = conversions.pivot_table(index=index, columns='loan_category',
#                                                   values='goal', aggfunc='count', fill_value=0)
#
#     pivoted_conversions = pivoted_conversions[['reg', 'new', 'rep']]
#
#     pivoted_budget = conversions.pivot_table(index=index, columns='loan_category',
#                                              values='payouts', aggfunc='sum', fill_value=0)
#
#     pivoted_budget.drop(columns=['reg'], inplace=True)
#
#     pivoted_budget.rename(columns={'new': 'costs_new', 'rep': 'costs_rep'}, inplace=True)
#
#     pivoted_budget['costs_total'] = pivoted_budget['costs_new'] + pivoted_budget['costs_rep']
#
#     conversions_final_df = pd.merge(pivoted_conversions, pivoted_budget, how='left', left_index=True, right_index=True)
#
#     # clicks = get_clicks_data(advertiser=advertiser, aff=aff, web=web, date_from=date_from, date_to=date_to)
#     # clicks = clicks.groupby(by=index).agg({'clicks': 'sum'})
#     #
#     # merged_data = pd.merge(clicks, conversions_final_df, how='left', left_index=True, right_index=True)
#     #
#     # merged_data['CR%'] = ((merged_data['reg'] / merged_data['clicks']) * 100).round(1)
#     # merged_data['AR%'] = ((merged_data['new'] / merged_data['reg']) * 100).round(1)
#     # merged_data['RLS%'] = ((merged_data['rep'] / (merged_data['new'] + merged_data['rep'])) * 100).round(1)
#     # merged_data['EPC'] = (merged_data['costs_total'] / merged_data['clicks']).astype(int)
#     # merged_data['CPAn'] = (merged_data['costs_new'] / merged_data['new']).astype(int)
#     # merged_data['CPAr'] = (merged_data['costs_total'] / merged_data['new']).astype(int)
#
#     return conversions, conversions_final_df