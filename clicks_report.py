import requests
import time
import json


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


start_date = '2020-03-11'
end_date = '2020-03-11'
lmt = 5000

pages = get_clicks_data(date_from=start_date, date_to=end_date, limit=1, page=1)['pagination']['total_count'] // lmt + 1

final_list = {
	'clicks': []
}
start = time.time()
for page in range(pages):
	raw_data = get_clicks_data(date_from=start_date, date_to=end_date, limit=lmt, page=(page + 1))
	for i in range(len(raw_data['clicks'])):
		offer_id = raw_data['clicks'][i]['offer']['id']
		click = raw_data['clicks'][i]
		if offer_id == 15:
			payload = {
				'device': click.get('device'),
				'device_type': click.get('device_type'),
				'device_model': click.get('device_model'),
				'os_fullname': click.get('os_fullname'),
				'city': click.get('city'),
				'sub3': click.get('sub3'),
				'partner_id': click.get('partner_id'),
				'partner_name': click.get('partner').get('name'),
				'has_conversions': click.get('has_conversions')
				}
			final_list['clicks'].append(payload)
	print('ready for: ', round((raw_data['pagination']['page'] / pages) * 100, 2), '%')

final_list.update({'clicks_count': len(final_list['clicks'])})

with open('offer14.json', 'w') as file:
	json.dump(final_list, file)
