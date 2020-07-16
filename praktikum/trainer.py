import pandas as pd
from pymystem3 import Mystem
from collections import Counter

m = Mystem()

client_data = pd.read_csv('data.csv')

# Обработка пропусков
for employee in client_data['income_type'].unique():
    median_income = client_data[client_data['income_type'] == employee]['total_income'].median()
    client_data.loc[(client_data['income_type'] == employee) & (client_data['total_income'].isnull()), 'total_income'] = median_income
print(client_data.info())

# columns = client_data.columns
#
# for column in columns:
#     if client_data.dtypes[column] == 'object':
#         client_data[column] = client_data[column].str.lower()
#
# # Смена типов данных
# client_data['total_income'] = client_data['total_income'].astype(int)
#
# # Удаление дубликатов
# client_data = client_data.drop_duplicates().reset_index(drop=True)
#
#
# # def get_lemma(row: str):
# #     lemma = m.lemmatize(row)[-2]
# #     return lemma
#
#
# # def create_income_category(total_income: int):
# #     if total_income <= 100000:
# #         return 'ниже среднего'
# #     elif 100000 < total_income <= 200000:
# #         return 'средний'
# #     elif 200000 < total_income <= 300000:
# #         return 'выше среднего'
# #     elif 300000 < total_income <= 400000:
# #         return 'высокий'
# #     return 'очень высокий'
#
#
# # # создаю новый ДФ группировкой данных по цели кредита, считаю для каждой цели кол-во кредитов и количество невозвратов
#
# # debt_purpose = client_data
# # debt_purpose.loc[(debt_purpose['purpose'] == 'покупка жилья для сдачи') | (debt_purpose['purpose'] == 'покупка жилья для семьи'), 'purpose'] = 'покупка жилья'
# # debt_purpose['purpose'] = debt_purpose['purpose'].apply(get_lemma)
# # debt_purpose.loc[debt_purpose['purpose'] == 'жилье', 'purpose'] = 'недвижимость'
# # debt_purpose = debt_purpose.pivot_table(index='purpose', columns='debt', values='total_income', aggfunc='count', margins=True, margins_name='total_loans')
# # debt_purpose.rename(columns={0: 'good_loans', 1: 'bad_loans'}, inplace=True)
# # debt_purpose['fail_cr%'] = debt_purpose['bad_loans'] / debt_purpose['total_loans'] * 100
# #
# # print(debt_purpose)
#
# # purpose_slice = client_data.groupby('purpose', as_index=False).agg({'total_income': 'count', 'debt': 'sum'})
# #
# # # создаю копию столбца цели кредита
# # purpose_slice.loc[:, 'new_purpose'] = purpose_slice['purpose']
# #
# # # изменяю цель кредита в индексах 19 и 20 столбца new_purpose
# # purpose_slice.loc[
# #     (purpose_slice['new_purpose'] == 'покупка жилья для сдачи') |
# #     (purpose_slice['new_purpose'] == 'покупка жилья для семьи'), 'new_purpose'] = 'покупка жилья'
# #
# # # лемматизирую строки в столбце и осталвяю последний элемент
# # purpose_slice['new_purpose'] = purpose_slice['new_purpose'].apply(get_lemma)
# #
# # # повторно группирую по цели кредита и суммирую сзначения в столбцах
# # purpose_slice = purpose_slice.groupby(by='new_purpose', as_index=False)[['total_income', 'debt']].sum()
# #
# # # добавляю столцем с CR%
# # purpose_slice['fail_cr%'] = round(purpose_slice['debt'] / purpose_slice['total_income'] * 100, 2)
# # print(purpose_slice)
# # # print(purpose_slice.sort_values(by='fail_cr%', ascending=False))
# # # print(purpose_slice['total_income'].sum())
# # # print(purpose_slice['debt'].sum())
#
# #
# # income = client_data
# # income['income_category'] = client_data['total_income'].apply(create_income_category)
# # income = income.pivot_table(index='income_category', columns='debt', values='total_income', aggfunc='count', margins=True, margins_name='total_loans')
# # income.rename(columns={0: 'good_loans', 1: 'bad_loans'}, inplace=True)
# # income['fail_cr%'] = income['bad_loans'] / income['total_loans'] * 100
# # print(income)
#
# # family_status = client_data.copy()
# # family_status = family_status.pivot_table(index='family_status', columns='debt', values='total_income', aggfunc='count', margins=True, margins_name='total_loans')
# # family_status.rename(columns={0: 'good_loans', 1: 'bad_loans'}, inplace=True)
# # family_status['fail_cr%'] = round(family_status['bad_loans'] / family_status['total_loans'] * 100, 2)
# # print(family_status)
# # print()
# # print(client_data)
#
# children = client_data
# indexes_out = children[(children['children'] == 20) | (children['children'] == -1)].index
# children.drop(indexes_out, inplace=True)
# children.loc[children['children'] >= 3, 'children'] = '3+'
# children = children.pivot_table(index='children', columns='debt', values='total_income', aggfunc='count', margins=True, margins_name='total_loans')
# children.rename(columns={0: 'good_loans', 1: 'bad_loans'}, inplace=True)
# children['fail_cr%'] = round(children['bad_loans'] / children['total_loans'] * 100, 2)
# print(children)

# for column in client_data.columns:
#     print(column)
#     print(client_data[column].value_counts(), end='\n\n')
# print(client_data[client_data['income_type'] == 'сотрудник'].info())
# print()
# one = client_data[client_data['income_type'] == 'сотрудник']['total_income'].reset_index(drop=True)
# one.to_csv('1.csv')
# print(one.median())
# two = client_data[client_data['income_type'] == 'сотрудник']['total_income'].dropna().reset_index(drop=True)
# two.to_csv('2.csv')
# print(two.median())
