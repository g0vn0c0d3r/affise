from Affise.final import *


lime_cpa = 7
konga_cpa = 8
lime_cpl = 15

date_from = '2020-06-01'
date_to = '2020-06-31'

partners_report = get_partners_daily_stats(offer_id=lime_cpa, date_from=date_from, date_to=date_to)
print(partners_report)
print()

monthly_rep = get_aggregated_affiliate_stats(offer_id=lime_cpa, date_from=date_from, date_to=date_to)
rep1 = monthly_rep[['raw_clicks', 'conversions', 'loans', 'CR%', 'AR%']].sort_values(by='loans', ascending=False)
rep2 = monthly_rep[['conversions', 'loans', 'cost', 'CPL', 'CPA', 'EPC']].sort_values(by='loans', ascending=False)
print(rep1)
print()
print(rep2)
print()
