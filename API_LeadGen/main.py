import requests
import time


file = open('LIME RU. Blocked 09.06.20.csv').readlines()
TOKEN = 'zbT1YLJGsEngsYAwI6a5iyx7Bz3qcktPQSy38Sp47zjKfdlJMDlrxn5B34ZfGOiG'

check_list = []
for contact in file:
    contact = contact.strip().split(';')
    check_list.append(contact)

count = 0
for item in check_list:
    mail = item[0]
    phone = item[1]

    resp = requests.get(f'https://zaim.io/api/denial?api_token={TOKEN}&items[phone]={phone}&items[email]={mail}')
    time.sleep(5)
    if resp.status_code == 200:
        count += 1
    print(f'{count} - {resp.status_code}')
print()
print(count)

