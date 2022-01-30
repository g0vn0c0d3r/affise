from basic_stats import *
import datetime

date_from = '2022-01-01'
date_to = '2022-01-05'
# date_to = str(datetime.date.today())


lime_stats = get_conversions_data(advertiser=LIME, aff='0', web='0',
                                  date_from=date_from, date_to=date_to, groupby='date')


aff = '29'
web = '0'

if web == '0':
    if aff != '0':
        lime_stats = lime_stats.query('partner == @aff')
    else:
        lime_stats = lime_stats
else:
    lime_stats = lime_stats.query('partner_id == @aff and sub3 == @web')

print(lime_stats)