from Affise.Offer import Offer
from Affise.Constants import OfferId


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

result = lime.get_aggregated_monthly_stats(date_from='2020-06-01', date_to='2020-06-31')
# result['Расход'] = result['Займ средний'] * 1800 + result['Займ хороший'] * 3000
# result['CPA'] = round(result['Расход'] / result['All'])
print(result)
