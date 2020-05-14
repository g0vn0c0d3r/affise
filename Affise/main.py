from Affise.Offer import Offer
from Affise.Constants import OfferId
from Affise.Constants import ConversionStatus


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

# lime.get_csv_reports(date_from='2020-04-01', date_to='2020-04-30')
# print(lime.get_pivot_sverka(date_from='2020-05-01', date_to='2020-05-30'))
# print(lime.api_conversions_request(date_from='2020-04-01', date_to='2020-04-30', status=1, limit=10, page=1))

