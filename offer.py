import requests
from datetime import date


class Offer:
	def __init__(self, *, offer_id, date_from='2020-02-15', date_to=date.today()):
		self.offer_id = offer_id
		self._api_url = 'https://api-lime-finance.affise.com/'
		self._api_key = 'c666e444eabc1706574ec7973ae4e677'
		self._raw_data = requests.get(
			self._api_url + '3.0/stats/custom',
			headers={'API-Key': self._api_key},
			params=(
				('slice[]', ['sub3', 'affiliate', 'year', 'month', 'day']),
				('filter[date_from]', date_from),
				('filter[date_to]', date_to),
				('filter[offer]', self.offer_id)
				)
			)

	def get_partner_list(self):
		partners = []
		for i in range(len(self._raw_data.json()['stats'])):
			if self._raw_data.json()['stats'][i]['slice']['affiliate']['id'] not in partners:
				partners.append(self._raw_data.json()['stats'][i]['slice']['affiliate']['id'])
		return sorted(partners)
