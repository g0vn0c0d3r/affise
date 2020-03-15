import requests

api_url = 'https://api-lime-finance.affise.com/'
api_key = 'c666e444eabc1706574ec7973ae4e677'


def get_raw_data(*, date_from, date_to, offer, limit, page):
    r = requests.get(
        api_url + '3.0/stats/conversions',
        headers={'API-Key': api_key},
        params=(
            ('date_from', date_from),
            ('date_to', date_to),
            ('offer', offer),
            ('limit', limit),
            ('page', page),
        )
    ).json()

    return r


pages = get_raw_data(
    date_from='2020-02-15',
    date_to='2020-03-14',
    offer=15,
    limit=1,
    page=1)['pagination']['total_count'] // 1000 + 1


conversions_list = []
for page in range(pages):
    req = get_raw_data(date_from='2020-02-15', date_to='2020-03-14', offer=15, limit=1000, page=(page + 1))
    for conversion in req['conversions']:
        affiliate = conversion['partner']['id']
        webmaster = conversion['sub3']
        registration = 1 if conversion['goal_value'] == '1' else 0
        loan = 1 if conversion['goal_value'] == '2' else 0

        revenue = conversion['revenue']

        payload = {
            'affiliate': affiliate,
            'webmaster': webmaster,
            'registrations': registration,
            'loans': loan,
            'revenue': revenue

        }

        conversions_list.append(payload)

final_list = []
for i in range(len(conversions_list)):
    payload = {
        'affiliate': conversions_list[i]['affiliate'],
        'webmaster': conversions_list[i]['webmaster'],
        'registrations': 0,
        'loans': 0,
        'revenue': 0
    }
    if payload not in final_list:
        final_list.append(payload)

for i in range(len(conversions_list)):
    for j in range(len(final_list)):
        if final_list[j]['affiliate'] == conversions_list[i]['affiliate'] and final_list[j]['webmaster'] == conversions_list[i]['webmaster']:
            final_list[j]['registrations'] += conversions_list[i]['registrations']
            final_list[j]['loans'] += conversions_list[i]['loans']
            final_list[j]['revenue'] += conversions_list[i]['revenue']


for i in sorted(final_list, key=lambda x: x['revenue'], reverse=True):
    print(i)
