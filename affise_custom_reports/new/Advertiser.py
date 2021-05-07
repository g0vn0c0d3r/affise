import requests
import pandas as pd
import Config


def create_data_frame(input_data: list):
    conversion_list = []
    columns = ['date', 'action_id', 'click_id', 'status', 'offer_id', 'goal', 'payouts',
               'partner', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6']

    for item in input_data:
        date = item['created_at'].split(' ')[0]
        action_id = item['action_id']
        click_id = item['clickid']
        status = item['status']
        offer_id = item['offer_id']
        goal = item['goal']
        payouts = item['payouts']
        partner = item['partner']['name']
        sub1 = item['sub1']
        sub2 = item['sub2']
        sub3 = item['sub3']
        sub4 = item['sub4']
        sub5 = item['sub5']
        sub6 = item['sub6']

        conversion_list.append([date, action_id, click_id, status, offer_id, goal, payouts,
                                partner, sub1, sub2, sub3, sub4, sub5, sub6])

    data_frame = pd.DataFrame(data=conversion_list, columns=columns)

    return data_frame


class Advertiser:

    def __init__(self, adv_id):
        self.adv_id = adv_id

    def api_single_request(self, date_from: str, date_to: str, rep_type: str, limit=1, page=1):

        if rep_type == 'conversions':
            report_type = Config.ReportType.CONVERSIONS.value
        else:
            report_type = Config.ReportType.CLICKS.value

        response = requests.get(Config.Credentials.API_URL.value + report_type,
                                headers={'API-Key': Config.Credentials.API_KEY.value},
                                params=(
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('advertiser', self.adv_id),
                                    ('limit', limit),
                                    ('page', page)
                                )).json()
        return response

    def create_conversions_list(self, date_from: str, date_to: str, pages: int):
        conversion_list = []
        for page in range(pages):
            conversions = self.api_single_request(date_from=date_from,
                                                  date_to=date_to,
                                                  rep_type='conversions',
                                                  page=page + 1,
                                                  limit=Config.Credentials.LIMIT.value)['conversions']
            conversion_list.extend(conversions)

        return conversion_list

    #TODO: Дописать метод группировки
    def daily_stats(self, date_from: str, date_to: str):
        pages = self.api_single_request(date_from=date_from,
                                        date_to=date_to,
                                        rep_type='conversions')['pagination'][
                    'total_count'] // Config.Credentials.LIMIT.value + 1

        conversion_list = self.create_conversions_list(date_from=date_from, date_to=date_to, pages=pages)

        data_frame = create_data_frame(input_data=conversion_list)

        return data_frame
