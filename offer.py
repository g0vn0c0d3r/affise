import requests


class Offer:
	def __init__(self, offer_id):
		self.offer_id = offer_id
		self.api_url = 'https://api-lime-finance.affise.com/'
		self.api_key = 'c666e444eabc1706574ec7973ae4e677'

	def get_partner_list(self, *, start_date: str, end_date: str) -> list:
		r = requests.get(
			self.api_url + '3.0/stats/getbypartner',
			headers={'API-Key': self.api_key},
			params=(
				('filter[date_from]', start_date),
				('filter[date_to]', end_date),
				('filter[offer]', self.offer_id)
				)).json()

		partner_list = []

		for i in range(len(r['stats'])):
			if r['stats'][i]['slice']['affiliate'] is not None:
				partner_list.append(r['stats'][i]['slice']['affiliate']['id'])

		return partner_list

	def get_webmaster_list(self, *, start_date: str, end_date: str):
		r = requests.get(
			self.api_url + '3.0/stats/custom',
			headers={'API-Key': self.api_key},
			params=(
				('slice[]', 'sub3'),
				('filter[date_from]', start_date),
				('filter[date_to]', end_date),
				('filter[offer]', self.offer_id)
				)).json()

		webmaster_list = []
		for i in range(len(r['stats'])):
			if r['stats'][i]['slice']['sub3'].isdigit():
				webmaster_list.append(int(r['stats'][i]['slice']['sub3']))

		return sorted(webmaster_list)
