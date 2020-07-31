import pandas as pd
import numpy
import matplotlib.pyplot as plt

raw_data = pd.read_csv('real_estate_data.csv', sep='\t')
data = raw_data

# пустые значения в ceiling_height заполняем медианой всего столбца
data['ceiling_height'].fillna(value=data['ceiling_height'].median(), inplace=True)

# пустые значения в living_area заполняем медианой с учетом количества комнат в помещении
for room in data['rooms'].unique():
    living_share = data[data['rooms'] == room]['living_area'].median() / data[data['rooms'] == room]['total_area'].median()
    data.loc[(data['living_area'].isna()) & (data['rooms'] == room), 'living_area'] = data['total_area'] * living_share

# свободная площать = общая площадь - жилая площадь
free_area = data['total_area'] - data['living_area']

# доля кухни = медиана площади кухни / медиану свободной площади
kitchen_share = data['kitchen_area'].median() / free_area.median()
data['kitchen_area'].fillna(free_area * kitchen_share, inplace=True)

# в столбце locality_name пропущено всего 49 значений, заменим их на "другое"
data['locality_name'].fillna('другое', inplace=True)

'''
Будем заполнять пропущенные значение медианой с учетом местоположения.
Но, т.к уникальных местоположений много,а данных по некоторым из них мало (или вообще нет) заменять буду так:
- для каждой локации делаем срез
- если в срезе есть 30+ не пустых значений --> заполняем медианой текущий локации
- для всех других локаций заполним пропуски общей медианой
'''

for locality in data['locality_name'].unique():
    if data[data['locality_name'] == locality]['cityCenters_nearest'].notnull().sum() > 30:
        median = data[data['locality_name'] == locality]['cityCenters_nearest'].median()
        data.loc[(data['locality_name'] == locality) & (data['cityCenters_nearest'].isnull()), 'cityCenters_nearest'] = median
    else:
        median = data['cityCenters_nearest'].median()
        data.loc[(data['locality_name'] == locality) & (data['cityCenters_nearest'].isnull()), 'cityCenters_nearest'] = median

data['days_exposition'].fillna(data['days_exposition'].median(), inplace=True)

# изменяем типы данных и округляем значения в 2 столбцах
for col in ['last_price', 'cityCenters_nearest', 'days_exposition']:
    data[col] = data[col].astype(int)

for col in ['living_area', 'kitchen_area']:
    data[col] = data[col].round(decimals=2)

data['first_day_exposition'] = pd.to_datetime(data['first_day_exposition'], format='%Y.%m.%d')

# ppsm = price per square meter
data['ppsm'] = round(data['last_price'] / data['total_area'], 0)

# living_share = отношение жилой площади к общей
data['living_share'] = round(data['living_area'] / data['total_area'], 2)

# kitchen_share = отношение жилой площади к общей
data['kitchen_share'] = round(data['kitchen_area'] / data['total_area'], 2)

# добавляем название и индекс дня недели
data['weekday_name'] = pd.DatetimeIndex(data['first_day_exposition']).day_name()
data['weekday_index'] = pd.DatetimeIndex(data['first_day_exposition']).weekday

# добавляем название и индекс месяца
data['month_name'] = pd.DatetimeIndex(data['first_day_exposition']).month_name()
data['month_index'] = pd.DatetimeIndex(data['first_day_exposition']).month

# добавляем год
data['year'] = pd.DatetimeIndex(data['first_day_exposition']).year


# категоризируем этажность
def get_floor_category(table):
    floors_total = table['floors_total']
    floor = table['floor']

    if floors_total == floor:
        return 'последний'
    elif floor == 1:
        return 'первый'
    else:
        return 'другой'


data['floor_category'] = data.apply(get_floor_category, axis=1)

# отфильтруем редкие значения и выбросы
data = data.query('30 < total_area < 150').reset_index(drop=True)

# удаляем редкие этажи
data = data.query('0 < rooms < 6').reset_index(drop=True)

# удаляем редкие этажи
data = data.query('2.4 < ceiling_height < 3.5').reset_index(drop=True)

# удаляем неадекватную стоимость квадратного метра
data = data.query('50000 < ppsm < 200000').reset_index(drop=True)





























