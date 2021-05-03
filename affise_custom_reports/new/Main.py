from Advertiser import *
import datetime


LIME = '5a558391c3ebae42008b4567'
KONGA = '5a558967c3ebae43008b4567'

lime = Advertiser(id=LIME)

start_date = '2021-03-01'
end_date = str(datetime.date.today())

# print(lime.single_api_conversions_request(date_from=start_date, date_to=end_date))
print(lime.create_conversions_list(date_from=start_date, date_to=end_date))
