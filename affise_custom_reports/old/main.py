from affise_manual_scripts.final import *
from affise_custom_reports.old.Offer import *

lime_cpa = 16
konga_cpa = 17
lime_cpl = 15

lime = Offer(offer_id=lime_cpa)
konga = Offer(offer_id=konga_cpa)

date_from = '2021-03-01'
date_to = '2021-03-31'

# konga = Offer(offer_id=konga_cpa)
# konga.get_csv_reports(date_from=date_from, date_to=date_to, path='reports/konga/july/')

print(get_stats_by_day(offer_id=lime_cpa, date_from=date_from, date_to=date_to))
print()
print(get_stats_by_day(offer_id=konga_cpa, date_from=date_from, date_to=date_to))
# print()
# partners_report = get_daily_stats_by_affiliate(offer_id=lime_cpa, date_from=date_from, date_to=date_to)
# print(partners_report)
# print()
#
# monthly_rep = get_aggregated_affiliate_stats(offer_id=lime_cpa, date_from=date_from, date_to=date_to)
# rep1 = monthly_rep[['raw_clicks', 'conversions', 'loans', 'CR%', 'AR%']].sort_values(by='loans', ascending=False)
# rep2 = monthly_rep[['conversions', 'loans', 'cost', 'CPL', 'CPA', 'EPC']].sort_values(by='loans', ascending=False)
# print(rep1)
# print()
# print(rep2)
# print()

# lime.get_csv_reports(date_from='2020-07-01', date_to='2020-07-31', path='reports/june')

# res = get_conversions_and_cost_by_webmaster(offer_id=lime_cpa, date_from=date_from, date_to=date_to, partner_id=30)
# print(res)
# res.to_csv('lg.cvs')
