import pandas as pd

data = pd.read_csv('lg.csv')

data = data[['Оффер', 'Выплата', 'SubID 1', 'SubID 2', 'Статус']]


def get_score(score_line: str):
    return score_line.split('|')[1]


approved_conversions = data[data['Статус'] == 'Одобрено'].dropna().reset_index(drop=True)
approved_conversions['SubID 2'] = approved_conversions['SubID 2'].apply(get_score)
approved_conversions['SubID 2'] = pd.to_numeric(approved_conversions['SubID 2'], errors='coerce')
approved_conversions = approved_conversions.dropna().reset_index(drop=True)
approved_conversions['Выплата'] = pd.to_numeric(approved_conversions['Выплата'], errors='coerce').astype(int)
approved_conversions.rename(columns={
    'Оффер': 'offer',
    'Выплата': 'payment',
    'SubID 1': 'source',
    'SubID 2': 'score',
    'Статус': 'status'
}, inplace=True)
approved_conversions['score1'] = approved_conversions['score']
approved_conversions = approved_conversions.groupby(by='offer').agg({
    'score': 'mean',
    'score1': 'median',
    'offer': 'count',
    'payment': 'sum'
}).sort_values('payment', ascending=False)

print(approved_conversions)
print(approved_conversions.to_csv('11.csv'))
