import requests
import time


api_url = 'https://api-lime-finance.affise.com/'
api_key = 'c666e444eabc1706574ec7973ae4e677'


def get_clicks_data(*, date_from: str, date_to: str, limit: int, page: int):
	response = requests.get(
		api_url + '3.0/stats/clicks',
		headers={'API-Key': api_key},
		params=(
			('date_from', date_from),
			('date_to', date_to),
			('limit', limit),
			('page', page)
			)
		).json()
	return response


lim = 5000
pg = 1
final_result = []

start1 = time.time()
while len(get_clicks_data(date_from='2020-03-10', date_to='2020-03-10', limit=lim, page=pg)['clicks']) != 0:
	start = time.time()
	raw_data = get_clicks_data(date_from='2020-03-10', date_to='2020-03-10', limit=lim, page=pg)
	for click in raw_data['clicks']:
		final_result.append(click)
	pg += 1
	print(raw_data['pagination'])
	print(time.time() - start1, end='\n')


print(time.time() - start1)
print(len(final_result))
