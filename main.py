from offer import Offer


lime_cpl = Offer(offer_id=15)

print(lime_cpl.offer_id)

print(lime_cpl.get_partner_list(start_date='2020-02-15', end_date='2020-03-04'))

print(lime_cpl.get_webmaster_list(start_date='2020-02-15', end_date='2020-03-04'))
