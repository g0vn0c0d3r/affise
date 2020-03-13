import requests
import time
import json


api_url = 'https://api-lime-finance.affise.com/'
api_key = 'c666e444eabc1706574ec7973ae4e677'

response = requests.get(
	api_url + '3.0/stats/custom',
	headers={'API-Key': api_key},
	params=(
		('slice[]', ['affiliate', 'sub3']),
		('filter[date_from]', '2020-03-01'),
		('filter[date_to]', '2020-03-11'),
		('filter[offer]', 15),
		# ('limit', 1)
		)).json()

print(response)
