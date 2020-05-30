from Affise.Offer import Offer
from Affise.Constants import OfferId
from Affise.Constants import ConversionStatus
import pandas as pd


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

# lime.get_csv_reports(date_from='2020-04-01', date_to='2020-04-30')
print(lime.get_aggregated_monthly_stats(date_from='2020-05-30', date_to='2020-05-30'))
print()
print(lime.get_daily_stats(date_from='2020-05-30', date_to='2020-05-30').iloc[:, 0:7])
