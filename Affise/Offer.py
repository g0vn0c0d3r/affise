import Affise.Constants


class Offer:
    PAGE_LIMIT = 5000

    def __init__(self, offer_id):
        self.offer_id = offer_id


Lime = Offer(Affise.Constants.OfferId.lime.value)

print(Lime.offer_id)
