from Affise.Offer import Offer
from Affise.Constants import OfferId
from Affise.Constants import ConversionStatus


lime = Offer(offer_id=OfferId.lime.value)
konga = Offer(offer_id=OfferId.konga.value)

lm = lime.get_csv_for_all_partners(date_from='2020-04-01', date_to='2020-04-30')
print(lm)

