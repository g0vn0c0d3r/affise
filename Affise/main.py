from Affise.Offer import Offer
from Affise.Constants import OfferId
from datetime import date


start = '2020-06-01'
end = date.today()

lime_cps = Offer(offer_id=OfferId.lime.value)
lime_cpl = Offer(offer_id=15)


aggr_stats = lime_cps.get_aggregated_monthly_stats(date_from=start, date_to=end)
print(aggr_stats)
