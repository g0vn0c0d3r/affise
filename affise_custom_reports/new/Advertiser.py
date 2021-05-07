import requests
import pandas as pd
import Config


def create_data_frame(input_data: list):
    conversion_list = []
    columns = ['ts', 'action_id', 'status']

    for item in input_data:
        ts = item['created_at']
        action_id = item['action_id']
        status = item['status']

        conversion_list.append([ts, action_id, status])

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
