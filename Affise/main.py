from Affise.final import *


lime_id = 7
konga_id = 8

date_from = '2020-06-01'
date_to = '2020-06-31'

partners_report = get_partners_daily_stats(offer_id=lime_id, date_from=date_from, date_to=date_to)
print(partners_report)
print()

monthly_rep = get_aggregated_affiliate_stats(offer_id=lime_id, date_from=date_from, date_to=date_from)
rep1 = monthly_rep[['raw_clicks', 'conversions', 'loans', 'CR%', 'AR%']].sort_values(by='loans', ascending=False)
rep2 = monthly_rep[['conversions', 'loans', 'cost', 'CPL', 'CPA']].sort_values(by='loans', ascending=False)
print(rep1)
print()
print(rep2)
print()
