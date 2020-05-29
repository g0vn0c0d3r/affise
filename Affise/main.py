from Affise.Offer import Offer
from Affise.Constants import OfferId


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

# print(lime.get_aggregated_monthly_stats(date_from='2020-04-01', date_to='2020-04-31'))
# print()
# print(konga.get_aggregated_monthly_stats(date_from='2020-04-01', date_to='2020-04-31'))

print(lime.get_aggregated_monthly_stats(date_from='2020-05-01', date_to='2020-05-30'))
print()
result = lime.get_daily_stats(date_from='2020-05-01', date_to='2020-05-30')
print(result.iloc[:, 0:7])
