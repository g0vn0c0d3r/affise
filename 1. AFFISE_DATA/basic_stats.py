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


def get_conversions_dataframe(advertiser: str, aff: str, web: str, date_from: str, date_to: str):

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

    return conversions_dataframe



    #
    # # Создаем сводную таблицу с динамикой бюджета
    # pivoted_budget = df_conv.pivot_table(index='date', columns='loan_category',
    #                                      values='payouts', aggfunc='sum', fill_value=0).reset_index()
    #
    # # Удаляем столбец с регистрациями т.к они бесплатные
    # pivoted_budget.drop(columns=['reg'], inplace=True)
    #
    # # Перименовываем столбцы
    # pivoted_budget.rename(columns={'new': 'costs_new', 'rep': 'costs_rep'}, inplace=True)
    #
    # # Добавляем столбец с общим бюджетом
    # pivoted_budget['costs_total'] = pivoted_budget['costs_new'] + pivoted_budget['costs_rep']
    #
    # pivoted_budget['date'] = pd.to_datetime(pivoted_budget['date'])
    #
    #
    #
    #
    #
    #
    # clicks = requests.get(url=API_URL + '/3.0/stats/custom', headers={'API-Key': API_KEY},
    #                       params=(
    #                           ('slice[]', 'year'),
    #                           ('slice[]', 'month'),
    #                           ('slice[]', 'day'),
    #                           ('filter[date_from]', date_from),
    #                           ('filter[date_to]', date_to)
    #                       )).json()
    #
    # clicks_list = []
    # columns = ['date', 'clicks']
    # for item in clicks['stats']:
    #     date = f'{item["slice"]["year"]}-{item["slice"]["month"]}-{item["slice"]["day"]}'
    #     clicks = int(item['traffic']['uniq'])
    #
    #     clicks_list.append([date, clicks])
    #
    # df_clicks = pd.DataFrame(data=clicks_list, columns=columns)
    # df_clicks['date'] = pd.to_datetime(df_clicks['date'])
    #
    # output_data = pd.merge(df_clicks, pivoted_conversions, on='date')
    #
    # output_data['CR%'] = ((output_data['reg'] / output_data['clicks']) * 100).round(2)
    # output_data['AR%'] = ((output_data['new'] / output_data['reg']) * 100).round(2)
    #
    # output_data = pd.merge(output_data, pivoted_budget, on='date')
    #
    #
    # return output_data
