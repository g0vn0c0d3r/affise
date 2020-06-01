from Affise.Offer import Offer
from Affise.Constants import OfferId


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

lime.get_webmaster_daily_stats(date_from='2020-05-01', date_to='2020-05-31').to_csv('hhh.csv')

#
# print(lime.get_aggregated_monthly_stats(date_from='2020-06-01', date_to='2020-06-31'))
# print()
# result = lime.get_partners_daily_stat(date_from='2020-06-01', date_to='2020-06-31')
# print(result.iloc[:, 0:7])
print(hi)
