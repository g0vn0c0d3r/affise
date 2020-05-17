from Affise.Offer import Offer
from Affise.Constants import OfferId
from Affise.Constants import ConversionStatus
import pandas as pd


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)


# result = lime.get_aggregated_monthly_stats(date_from='2020-05-01', date_to='2020-05-30')

result = lime.get_daily_stats(date_from='2020-05-01', date_to='2020-05-30')
print(result.iloc[:, 0:7])
