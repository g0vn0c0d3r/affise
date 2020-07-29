import pandas as pd
import numpy
import matplotlib.pyplot as plt

raw_data = pd.read_csv('real_estate_data.csv', sep='\t')
data = raw_data
data['ceiling_height'].fillna(value=data['ceiling_height'].median(), inplace=True)

for room in data['rooms'].unique():
    living_share = data[data['rooms'] == room]['living_area'].median() / data[data['rooms'] == room]['total_area'].median()
    data.loc[(data['living_area'].isna()) & (data['rooms'] == room), 'living_area'] = data['total_area'] * living_share

free_area = data['total_area'] - data['living_area']
kitchen_share = data['kitchen_area'].median() / free_area.median()
data['kitchen_area'].fillna(free_area * kitchen_share, inplace=True)

# в столбце locality_name пропущено всего 49 значений, заменим их на "другое"
data['locality_name'].fillna('другое', inplace=True)


for locality in data['locality_name'].unique():
    if data[data['locality_name'] == locality]['cityCenters_nearest'].notnull().sum() > 30:
        median = data[data['locality_name'] == locality]['cityCenters_nearest'].median()
        data.loc[(data['locality_name'] == locality) & (data['cityCenters_nearest'].isnull()), 'cityCenters_nearest'] = median
    else:
        median = data['cityCenters_nearest'].median()
        data.loc[(data['locality_name'] == locality) & (data['cityCenters_nearest'].isnull()), 'cityCenters_nearest'] = median

print(data.isna().sum())



