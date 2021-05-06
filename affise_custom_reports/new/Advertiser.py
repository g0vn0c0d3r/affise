import requests
import pandas as pd
import Config


class Advertiser:

    def __init__(self, id):
        self.id = id

    def api_single_request(self, date_from: str, date_to: str, rep_type: str, limit=1, page=1):

        if rep_type == 'conversions':
            report_type = Config.ReportType.CONVERSIONS.value
        elif rep_type == 'clicks':
            report_type = Config.ReportType.CLICKS.value

        response = requests.get(Config.Credentials.API_URL.value + report_type,
                                headers={'API-Key': Config.Credentials.API_KEY.value},
                                params=(
                                    ('date_from', date_from),
                                    ('date_to', date_to),
                                    ('advertiser', self.id),
                                    ('limit', limit),
                                    ('page', page)
                                )).json()
        return response

    def create_conversions_list(self, date_from: str, date_to: str):
        pages = self.api_single_request(date_from=date_from,
                                        date_to=date_to,
                                        rep_type='conversions')['pagination']['total_count'] // Config.Credentials.LIMIT.value + 1

        conversion_list = []
        for page in range(pages):
            conversions = self.api_single_request(date_from=date_from,
                                                  date_to=date_to,
                                                  rep_type='conversions',
                                                  page=page + 1,
                                                  limit=Config.Credentials.LIMIT.value)['conversions']

            conversion_list.extend(conversions)
        return conversion_list
