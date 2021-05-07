from Advertiser import *
import datetime


LIME = '5a558391c3ebae42008b4567'
KONGA = '5a558967c3ebae43008b4567'

lime = Advertiser(adv_id=LIME)

start_date = '2021-05-01'
end_date = str(datetime.date.today())

lime = lime.daily_stats(date_from=start_date, date_to=end_date)

lime.sample(10).to_csv('TEST.csv')
