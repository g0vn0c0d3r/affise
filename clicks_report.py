import requests
import json
from datetime import date


api_url = 'https://api-lime-finance.affise.com/'
api_key = 'c666e444eabc1706574ec7973ae4e677'

response = requests.get(api_url + '3.0/stats/clicks',
						headers={'API-Key': api_key},
						params=(
							('date_from', date.today()),
							('date_to', date.today()),
							)
						).json()

clicks = response['pagination']['total_count']
pages = round(clicks / 100) + 1

final = []
for i in range(1, pages):
	final.append(requests.get(
		api_url + '3.0/stats/clicks',
		headers={'API-Key': api_key},
		params=(
			('date_from', date.today()),
			('date_to', date.today()),
			('page', i)
			)).json())

with open('data.json', 'w') as f:
	json.dump(final, f)
