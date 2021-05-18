import requests
import pandas as pd
import Config


def create_data_frame(input_data: list):
    conversion_list = []
    columns = ['date', 'action_id', 'click_id', 'status', 'offer_id', 'goal', 'payouts',
               'partner', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6']

    for item in input_data:
        date = item['created_at'].split(' ')[0]
        action_id = item['action_id']
        click_id = item['clickid']
        status = item['status']
        offer_id = item['offer_id']
        goal = item['goal']
        payouts = item['payouts']
        partner = item['partner']['name']
        sub1 = item['sub1']
        sub2 = item['sub2']
        sub3 = item['sub3']
        sub4 = item['sub4']
        sub5 = item['sub5']
        sub6 = item['sub6']

        conversion_list.append([date, action_id, click_id, status, offer_id, goal, payouts,
                                partner, sub1, sub2, sub3, sub4, sub5, sub6])

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
        'Займ средний': 'low_score_client',
        'Займ хороший': 'med_score_client',
        'Займ отличный': 'high_score_client',
        'Повторный займ': 'repeated_loan'
    }, inplace=True)

    # категоризайия займов
    data_frame['loan_category'] = data_frame.apply(goal_categorization, axis=1)

    return data_frame


def goal_categorization(row):
    goal = row['goal']

    if goal == 'registration':
        return 'reg'
    elif goal == 'repeated_loan':
        return 'old'
    else:
        return 'new'


class Advertiser:

    def __init__(self, adv_id):
        self.adv_id = adv_id

    def api_conversions_single_request(self, date_from: str, date_to: str, limit=1, page=1):
        response = requests.get(Config.Credentials.API_URL.value + Config.ReportType.CONVERSIONS.value,
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
            conversions = self.api_conversions_single_request(date_from=date_from,
                                                              date_to=date_to,
                                                              page=page + 1,
                                                              limit=Config.Credentials.LIMIT.value)['conversions']
            conversion_list.extend(conversions)

        return conversion_list

    def advertiser_general_stats(self, date_from: str, date_to: str, groupby: str):
        # Делаем 1 запрос в API и считаем кол-во страниц в ответе
        pages = self.api_conversions_single_request(
            date_from=date_from,
            date_to=date_to)['pagination']['total_count'] // Config.Credentials.LIMIT.value + 1

        # Собираем все конверсии в 1 общий список
        conversion_list = self.create_conversions_list(date_from=date_from, date_to=date_to, pages=pages)

        # Из списка конверсий собираем data frame
        data_frame = create_data_frame(input_data=conversion_list)

        # Генерируем сводную таблицу с конверсиями и группировкой по groupby
        pivoted_conversions = data_frame.pivot_table(index=groupby, columns='loan_category', values='goal',
                                                     aggfunc='count').reindex(['reg', 'new', 'old'], axis=1)

        # Добавляем расчитываемые параметры
        pivoted_conversions['total'] = pivoted_conversions['new'] + pivoted_conversions['old']
        pivoted_conversions['ARn%'] = (pivoted_conversions['new'] / pivoted_conversions['reg']).round(2)
        pivoted_conversions['ARo%'] = (pivoted_conversions['old'] / pivoted_conversions['reg']).round(2)
        pivoted_conversions['RLS%'] = (pivoted_conversions['old'] / pivoted_conversions['total']).round(2)

        # Генерируем сводную таблицу с бюджетами по разным типам займов и группировкой по groupby
        pivoted_budget = data_frame.pivot_table(index=groupby, columns='loan_category', values='payouts', aggfunc='sum')

        # Удаляем столбец 'reg'
        pivoted_budget.drop(columns='reg', inplace=True)

        # Переименовываем часть столбцов
        pivoted_budget.rename(columns={'new': 'costs_new', 'old': 'costs_old'}, inplace=True)

        # Считаем общий бюджет по всем типам займов
        pivoted_budget['costs_total'] = pivoted_budget['costs_new'] + pivoted_budget['costs_old']

        # Объединяем сводные таблицы с конверсиями и бюджетом
        merged_data = pd.merge(pivoted_conversions, pivoted_budget, how='left', on=groupby)

        # Добавялем расчитываемые показатели
        merged_data['CPAn'] = (merged_data['costs_new'] / merged_data['new']).astype('int')
        merged_data['CPAo'] = (merged_data['costs_old'] / merged_data['old']).astype('int')
        merged_data['CPAr'] = (merged_data['costs_total'] / merged_data['new']).astype('int')
        merged_data['CPL'] = (merged_data['costs_total'] / merged_data['reg']).astype('int')

        return merged_data

    def partner_general_stats(self, date_from: str, date_to: str, partner_id: int, groupby: str):
        # Делаем 1 запрос в API и считаем кол-во страниц в ответе
        pages = self.api_conversions_single_request(
            date_from=date_from,
            date_to=date_to)['pagination']['total_count'] // Config.Credentials.LIMIT.value + 1

        # Собираем все конверсии в 1 общий список
        conversion_list = self.create_conversions_list(date_from=date_from, date_to=date_to, pages=pages)

        # Из списка конверсий собираем data frame
        data_frame = create_data_frame(input_data=conversion_list)
        data_frame = data_frame[data_frame['partner'] == partner_id]

        # Генерируем сводную таблицу с конверсиями и группировкой по groupby
        pivoted_conversions = data_frame.pivot_table(index=groupby, columns='loan_category', values='goal',
                                                     aggfunc='count').reindex(['reg', 'new', 'old'], axis=1)

        # Добавляем расчитываемые параметры
        pivoted_conversions['total'] = pivoted_conversions['new'] + pivoted_conversions['old']
        pivoted_conversions['ARn%'] = (pivoted_conversions['new'] / pivoted_conversions['reg']).round(2)
        pivoted_conversions['ARo%'] = (pivoted_conversions['old'] / pivoted_conversions['reg']).round(2)
        pivoted_conversions['RLS%'] = (pivoted_conversions['old'] / pivoted_conversions['total']).round(2)

        # Генерируем сводную таблицу с бюджетами по разным типам займов и группировкой по groupby
        pivoted_budget = data_frame.pivot_table(index=groupby, columns='loan_category', values='payouts', aggfunc='sum')

        # Удаляем столбец 'reg'
        pivoted_budget.drop(columns='reg', inplace=True)

        # Переименовываем часть столбцов
        pivoted_budget.rename(columns={'new': 'costs_new', 'old': 'costs_old'}, inplace=True)

        # Считаем общий бюджет по всем типам займов
        pivoted_budget['costs_total'] = pivoted_budget['costs_new'] + pivoted_budget['costs_old']

        # Объединяем сводные таблицы с конверсиями и бюджетом
        merged_data = pd.merge(pivoted_conversions, pivoted_budget, how='left', on=groupby)

        # Добавялем расчитываемые показатели
        merged_data['CPAn'] = (merged_data['costs_new'] / merged_data['new']).astype('int')
        merged_data['CPAo'] = (merged_data['costs_old'] / merged_data['old']).astype('int')
        merged_data['CPAr'] = (merged_data['costs_total'] / merged_data['new']).astype('int')
        merged_data['CPL'] = (merged_data['costs_total'] / merged_data['reg']).astype('int')

        return merged_data
