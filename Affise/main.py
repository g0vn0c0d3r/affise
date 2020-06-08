from Affise.final import *


lime_id = 7

monthly_rep = get_aggregated_affiliate_stats(offer_id=lime_id, date_from='2020-06-01', date_to='2020-06-31')
print(monthly_rep.columns)
print(monthly_rep)
