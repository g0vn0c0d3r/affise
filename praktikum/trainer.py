import pandas as pd
from pymystem3 import Mystem
from collections import Counter

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
    m = Mystem()
    not_lemma = row.split()[-1]
    lemma = ''.join(m.lemmatize(not_lemma)).rstrip()
    return lemma

# lemmas = Counter(Mystem().lemmatize(' '.join(client_data['purpose'])))
# print(lemmas)


purpose_slice = client_data.groupby('purpose', as_index=False).agg({'total_income': 'count', 'debt': 'sum'})
print(purpose_slice)

