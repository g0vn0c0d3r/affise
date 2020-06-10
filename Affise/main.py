from Affise.final import *


lime_id = 7
konga_id = 8

date_from = '2020-05-09'
date_to = '2020-06-09'

# partners_report = get_partners_daily_stats(offer_id=lime_id, date_from=date_from, date_to=date_to)
# print(partners_report)
# print()
#
# monthly_rep = get_aggregated_affiliate_stats(offer_id=lime_id, date_from=date_from, date_to=date_to)
# rep1 = monthly_rep[['raw_clicks', 'conversions', 'loans', 'CR%', 'AR%']].sort_values(by='loans', ascending=False)
# rep2 = monthly_rep[['conversions', 'loans', 'cost', 'CPL', 'CPA', 'EPC']].sort_values(by='loans', ascending=False)
# print(rep1)
# print()
# print(rep2)
# print()
#
#
leadgid = get_webmasters_report(offer_id=lime_id, partner_id=30, date_from=date_from, date_to=date_to)
guruleads = get_webmasters_report(offer_id=lime_id, partner_id=34, date_from=date_from, date_to=date_to)
leadssu = get_webmasters_report(offer_id=lime_id, partner_id=29, date_from=date_from, date_to=date_to)


leadgid.to_csv('leadgid.csv')
guruleads.to_csv('guruleads.csv')
leadssu.to_csv('leadssu.csv')

# print()
# print(leadssu)
# print()
# print(guruleads)


