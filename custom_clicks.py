import requests
from datetime import date


api_url = 'https://api-lime-finance.affise.com/'
api_key = 'c666e444eabc1706574ec7973ae4e677'


clicks = requests.get(
	api_url + '3.0/stats/custom',
	headers={'API-Key': api_key},
	params=(
		('slice[]', ['affiliate', 'sub3']),
		('filter[date_from]', '2020-02-20'),
		('filter[date_to]', date.today()),
		('filter[offer]', 15),
	)
).json()

print(clicks)
