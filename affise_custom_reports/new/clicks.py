import requests
import time

headers = {
    'API-Key': '0a3994e5f04ed3d755cba60eb50de7c6',
}

start = time.time()
response = requests.get('https://api-lime-finance.affise.com/3.0/stats/custom?'
                        'slice[]=year'
                        '&slice[]=month'
                        '&slice[]=day'
                        # '&slice[]=affiliate'
                        # '&slice[]=sub3'
                        '&filter[date_from]=2021-01-01'
                        '&filter[date_to]=2021-12-16'
                        '&limit=500',
                        headers=headers).json()

print(response)
end = time.time()
print(end-start)