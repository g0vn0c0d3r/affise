import requests
from datetime import date


class Offer:
	def __init__(self, *, offer_id):
		self.offer_id = offer_id
		self._api_url = 'https://api-lime-finance.affise.com/'
		self._api_key = 'c666e444eabc1706574ec7973ae4e677'

	def get_partner_list(self, *, start_date: str, end_date: str):
		response = requests.get(self._api_url + '3.0/stats/getbypartner',
								headers={'API-Key': self._api_key},
								params=(
									('filter[date_from]', start_date),
									('filter[date_to]', end_date),
									('filter[offer]', self.offer_id)
									)
								).json()
		result = []
		for i in range(len(response['stats'])):
			if type(response['stats'][i]['slice']['affiliate']) is dict:
				result.append(response['stats'][i]['slice']['affiliate']['id'])
		return result
