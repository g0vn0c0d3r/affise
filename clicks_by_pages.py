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


start_date = '2020-03-10'
end_date = '2020-03-10'
lmt = 100

pages = get_clicks_data(date_from=start_date, date_to=end_date, limit=1, page=1)['pagination']['total_count'] // lmt + 1

final_list = []

start = time.time()

for page in range(pages):
	start = time.time()
	raw_data = get_clicks_data(date_from=start_date, date_to=end_date, limit=lmt, page=(page + 1))
	for click in raw_data['clicks']:
		final_list.append(click)
	print('ready for: ', round((raw_data['pagination']['page'] / pages) * 100, 2), '%')
	print()

print(time.time() - start)
print(len(final_list))
