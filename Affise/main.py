from Affise.Offer import Offer
from Affise.Constants import OfferId
from Affise.Constants import ConversionStatus


lime = Offer(offer_id=OfferId.lime.value)

# report = lime.api_conversions_request(date_from='2020-02-01', date_to='2020-04-30', status=ConversionStatus.confirmed.value)
# print(report)
# print(report['pagination'])

# print(lime.get_sverka(date_from='2020-02-01', date_to='2020-04-30'))
print(lime.create_conversion_list(pages=3, date_from='2020-02-01', date_to='2020-04-30'))
