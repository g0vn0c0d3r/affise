import requests
import pandas as pd
from datetime import datetime


API_URL = 'https://api-lime-finance.affise.com'
API_KEY = '0a3994e5f04ed3d755cba60eb50de7c6'
LIMIT = 5000
LIME_ADV_ID = '5a558391c3ebae42008b4567'
KONGA_ADV_ID = '5a558967c3ebae43008b4567'

date_from = '2021-12-15'
date_to = str(datetime.today())


clicks = requests.get(url=API_URL + '/3.0/stats/custom', headers={'API-Key': API_KEY},
                          params=(
                              ('slice[]', 'year'),
                              ('slice[]', 'month'),
                              ('slice[]', 'day'),
                              ('filter[date_from]', date_from),
                              ('filter[date_to]', date_to)
                          )).json()

# print(len(clicks['stats']))

# clicks_data = []
# for item in clicks['stats']:
#     # print(type(item['slice']['year']))
#     date = datetime.datetime.strptime(str(item['slice']['year']) + str(item['slice']['month']) + str(item['slice']['day']), format='%y-%m-%d')
#     print(date)
#     # clicks_data.extend(date)
#
# print(clicks_data)

print(datetime.fromisoformat('2021-12-15'))