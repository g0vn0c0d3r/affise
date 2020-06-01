from Affise.Offer import Offer
from Affise.Constants import OfferId
from datetime import date


start = '2020-06-01'
end = date.today()

lime_cps = Offer(offer_id=OfferId.lime.value)
lime_cpl = Offer(offer_id=15)


aggr_stats = lime_cps.get_aggregated_monthly_stats(date_from=start, date_to=end)
aggr_stats['Cost'] = aggr_stats['Займ средний'] * 1800 + aggr_stats['Займ хороший'] * 3000
aggr_stats['CPA'] = round(aggr_stats['Cost'] / aggr_stats['All'])
print(aggr_stats)
print()

daily = lime_cps.get_daily_stats(date_from=start, date_to=end)
daily['Cost'] = daily['Займ средний'] * 1800 + daily['Займ хороший'] * 3000
daily['CPA'] = round(daily['Cost'] / daily['All'])
print(daily)
print()

print(lime_cps.get_partners_daily_stats(date_from=start, date_to=end).iloc[:, :7])
print()


result = lime_cpl.get_aggregated_monthly_stats(date_from=start, date_to=end)
result['Cost'] = result['All'] * 200
print(result)
print()

result_2 = lime_cpl.get_daily_stats(date_from=start, date_to=end)
result_2['Cost'] = result_2['All'] * 200
# result_2['CPA'] = result_2['Cost'] / result_2['Займ']
print()

result_3 = lime_cpl.get_partners_daily_stats(date_from=start, date_to=end)
print(result_3)
