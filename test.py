import requests

headers = {
	'API-Key': 'c666e444eabc1706574ec7973ae4e677',
	}

params = (
	('slice[]', ['sub3', 'affiliate']),
	('filter[date_from]', '2020-02-15'),
	('filter[date_to]', '2020-03-04'),
	('filter[offer]', '15'),
	('limit', 1))

response = requests.get('https://api-lime-finance.affise.com/3.0/stats/custom', headers=headers, params=params).json()

print(response)
