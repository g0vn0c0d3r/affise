import pandas as pd
from pymystem3 import Mystem
from collections import Counter
m = Mystem()

client_data = pd.read_csv('data.csv')

# Обработка пропусков
for employee in client_data['income_type'].unique():
    median_income = client_data[client_data['income_type'] == employee]['total_income'].median()
    client_data.loc[(client_data['income_type'] == employee) & (client_data['total_income'].isnull()), 'total_income'] = median_income

# Смена типов данных
client_data['total_income'] = client_data['total_income'].astype(int)

# Удаление дубликатов
client_data = client_data.drop_duplicates().reset_index(drop=True)


def get_lemma(row: str):
    not_lemma = row.split()[-1]
    lemma = ''.join(m.lemmatize(not_lemma)).rstrip()
    return lemma


# lemmas = Counter(m.lemmatize(' '.join(client_data['purpose'])))
# for i in lemmas:
#     print(i, lemmas.get(i))


# # создаю новый ДФ группировкой данных по цели кредита, считаю для каждой цели кол-во кредитов и количество невозвратов
purpose_slice = client_data.groupby('purpose', as_index=False).agg({'total_income': 'count', 'debt': 'sum'})

# создаю копию столбца цели кредита
purpose_slice.loc[:, 'new_purpose'] = purpose_slice['purpose']

# изменяю цель кредита в индексах 19 и 20 столбца new_purpose
purpose_slice.loc[
    (purpose_slice['new_purpose'] == 'покупка жилья для сдачи') |
    (purpose_slice['new_purpose'] == 'покупка жилья для семьи'), 'new_purpose'] = 'покупка жилья'

# лемматизирую строки в столбце и осталвяю последний элемент
purpose_slice['new_purpose'] = purpose_slice['new_purpose'].apply(get_lemma)

# повторно группирую по цели кредита и суммирую сзначения в столбцах
purpose_slice = purpose_slice.groupby(by='new_purpose', as_index=False)[['total_income', 'debt']].sum()

# добавляю столцем с CR%
purpose_slice['fail_cr%'] = round(purpose_slice['debt'] / purpose_slice['total_income'] * 100, 2)
print(purpose_slice)
# print(purpose_slice.sort_values(by='fail_cr%', ascending=False))
# print(purpose_slice['total_income'].sum())
# print(purpose_slice['debt'].sum())

