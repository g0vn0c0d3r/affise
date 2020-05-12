from Affise.Offer import Offer
from Affise.Constants import OfferId
from Affise.Constants import ConversionStatus


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

lm = lime.get_sverka(date_from='2020-05-01', date_to='2020-05-30')
print(lm)
# print()
# kg = konga.get_sverka(date_from='2020-05-01', date_to='2020-05-30')
# print(kg)

