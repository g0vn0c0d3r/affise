import requests
import pandas as pd
import Config
import numpy as np


def create_data_frame(input_data: list):
    conversion_list = []
    columns = ['date', 'action_id', 'click_id', 'status', 'offer_id', 'goal', 'payouts',
               'partner', 'partner_id', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6']

    for item in input_data:
        date = item['created_at'].split(' ')[0]
        action_id = item['action_id']
        click_id = item['clickid']
        status = item['status']
        offer_id = item['offer_id']
        goal = item['goal']
        payouts = item['payouts']
        partner = item['partner']['name']
        partner_id = str(item['partner']['id'])
        sub1 = item['sub1']
        sub2 = item['sub2']
        sub3 = item['sub3']
        sub4 = item['sub4']
        sub5 = item['sub5']
        sub6 = item['sub6']

        conversion_list.append([date, action_id, click_id, status, offer_id, goal, payouts,
                                partner, partner_id, sub1, sub2, sub3, sub4, sub5, sub6])

    data_frame = pd.DataFrame(data=conversion_list, columns=columns)

    # приведем столбец date в нужный тип данных
    data_frame['date'] = data_frame['date'].astype('datetime64[D]')

    # выделяем из date новые столбцы: weekday, month, year
    data_frame['weekday'] = data_frame['date'].dt.day_name()
    data_frame['week'] = data_frame['date'].dt.isocalendar().week
    data_frame['month'] = data_frame['date'].dt.month
    data_frame['year'] = data_frame['date'].dt.year

    # переименовываем название целей в столбце goal
    data_frame['goal'].replace({
        'регистрация': 'registration',
        'регистрация 1': 'registration',
        'Займ средний': 'low_score_client',
        'Займ средний 2': 'low_score_client',
        'Займ хороший': 'med_score_client',
        'Займ хороший 3': 'med_score_client',
        'Займ отличный': 'high_score_client',
        'Займ отличный 4': 'high_score_client',
        'Повторный займ': 'repeated_loan'
    }, inplace=True)

    # категоризайия займов
    data_frame['loan_category'] = data_frame.apply(goal_categorization, axis=1)

    # удаляем статусы declined
    data_frame = data_frame[data_frame['status'] != 'declined']

    return data_frame


def goal_categorization(row):
    goal = row['goal']

    if goal == 'registration':
        return 'reg'
    elif goal == 'repeated_loan':
        return 'rep'
    else:
        return 'new'


def get_general_stats(data, index: str):
    # Создаем сводную таблицу с динамикой кол-ва конверсий в разбивке по типам
    pivoted_conversions = data.pivot_table(index=index, columns='loan_category', values='goal', aggfunc='count', fill_value=0)

    # Меняем очередность столбцов
    pivoted_conversions = pivoted_conversions[['reg', 'new', 'rep']]

    # Добавляем расчетные показатели
    pivoted_conversions['total'] = pivoted_conversions['new'] + pivoted_conversions['rep']
    pivoted_conversions['ARn%'] = (pivoted_conversions['new'] / pivoted_conversions['reg']).round(2)
    pivoted_conversions['ARr%'] = (pivoted_conversions['rep'] / pivoted_conversions['reg']).round(2)
    pivoted_conversions['RLS%'] = (pivoted_conversions['rep'] / pivoted_conversions['total']).round(2)

    # Создаем сводную таблицу с динамикой бюджета
    pivoted_budget = data.pivot_table(index=index, columns='loan_category', values='payouts', aggfunc='sum', fill_value=0)

    # Удаляем столбец с регистрациями т.к они бесплатные
    pivoted_budget.drop(columns=['reg'], inplace=True)

    # Перименовываем столбцы
    pivoted_budget.rename(columns={'new': 'costs_new', 'rep': 'costs_rep'}, inplace=True)

    # Добавляем столбец с общим бюджетом
    pivoted_budget['costs_total'] = pivoted_budget['costs_new'] + pivoted_budget['costs_rep']

    # Объеденям сводную с конверсиями и бюджетом
    merged_data = pd.merge(pivoted_conversions, pivoted_budget, how='left', on=index)

    # Добавляем расчетные показатели
    merged_data['CPAn'] = merged_data['costs_new'] / merged_data['new']
    merged_data['CPAo'] = merged_data['costs_rep'] / merged_data['rep']
    merged_data['CPAr'] = merged_data['costs_total'] / merged_data['new']

    # Меняем inf nan
    merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Меняем nan на 0
    merged_data.fillna(0, inplace=True)

    # Приводим столбцы со стоимостью к int, для округления
    merged_data['CPAn'] = merged_data['CPAn'].astype('int')
    merged_data['CPAo'] = merged_data['CPAo'].astype('int')
    merged_data['CPAr'] = merged_data['CPAr'].astype('int')

    return merged_data


def get_loans_by_aff(data, index: str):
    data = data.query('loan_category != "reg"')

    pivoted_data = data.pivot_table(
        index=index, columns='partner', values='goal',
        aggfunc='count', fill_value=0, margins=True).sort_values(by='All', axis=1, ascending=False)

    pivoted_data.drop(index='All', inplace=True)
    pivoted_data.drop(columns='All', inplace=True)

    return pivoted_data


class Advertiser:

    def __init__(self, adv_id):
        self.adv_id = adv_id

    def api_single_request(self, date_from: str, date_to: str, rep_type: str, limit=1, page=1):

        if rep_type == 'conversions':
            report_type = Config.ReportType.CONVERSIONS.value
        else:
            report_type = Config.ReportType.CLICKS.value

        response = requests.get(Config.Credentials.API_URL.value + report_type,
                                headers={'API-Key': Config.Credentials.API_KEY.value},
                                params=(
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('advertiser', self.adv_id),
                                    ('limit', limit),
                                    ('page', page)
                                )).json()
        return response

    def create_conversions_list(self, date_from: str, date_to: str, pages: int):
        conversion_list = []
        for page in range(pages):
            conversions = self.api_single_request(date_from=date_from,
                                                  date_to=date_to,
                                                  rep_type='conversions',
                                                  page=page + 1,
                                                  limit=Config.Credentials.LIMIT.value)['conversions']
            conversion_list.extend(conversions)

        return conversion_list

    def create_data_frame(self, date_from: str, date_to: str):
        pages = self.api_single_request(date_from=date_from,
                                        date_to=date_to,
                                        rep_type='conversions')['pagination'][
                    'total_count'] // Config.Credentials.LIMIT.value + 1

        conversion_list = self.create_conversions_list(date_from=date_from, date_to=date_to, pages=pages)

        data_frame = create_data_frame(input_data=conversion_list)

        return data_frame
