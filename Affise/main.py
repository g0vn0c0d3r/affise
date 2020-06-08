from Affise.final import *


lime_id = 7

monthly_rep = get_aggregated_affiliate_stats(offer_id=lime_id, date_from='2020-06-01', date_to='2020-06-31')

rep1 = monthly_rep[['raw_clicks', 'conversions', 'total_loans']].sort_values(by=['total_loans'], ascending=False)
rep1['CR%'] = round((rep1['conversions'] / rep1['raw_clicks']) * 100, 1)
rep1['AR%'] = round((rep1['total_loans'] / rep1['conversions']) * 100, 1)

print(rep1)
print()

rep2 = monthly_rep[['low', 'medium', 'total_loans', 'cost']].sort_values(by='total_loans', ascending=False)
rep2['cpa'] = round(rep2['cost'] / rep2['total_loans'])
print(rep2)

print()
print(monthly_rep.columns)

