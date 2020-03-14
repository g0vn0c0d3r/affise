data = [
    {'affiliate': 30, 'webmaster': 24489, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 1, 'loans': 0, 'revenue': 300},
    {'affiliate': 70, 'webmaster': 2024, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 70, 'webmaster': 157, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 70, 'webmaster': 2024, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 38645, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 25265, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 55562, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 25265, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 1, 'loans': 0, 'revenue': 300},
    {'affiliate': 70, 'webmaster': 329, 'registrations': 1, 'loans': 0, 'revenue': 500},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 1, 'loans': 0, 'revenue': 300},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 0, 'loans': 1, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 1, 'loans': 0, 'revenue': 300},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 1, 'loans': 0, 'revenue': 300},
    {'affiliate': 30, 'webmaster': 38645, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 1, 'loans': 0, 'revenue': 400},
    {'affiliate': 30, 'webmaster': 41259, 'registrations': 0, 'loans': 1, 'revenue': 200},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 0, 'loans': 1, 'revenue': 200},
    {'affiliate': 70, 'webmaster': 1603, 'registrations': 1, 'loans': 0, 'revenue': 200},
    {'affiliate': 70, 'webmaster': 16, 'registrations': 1, 'loans': 0, 'revenue': 300}]

data = sorted(data, key=lambda x: x['webmaster'])

for i in data:
    print(i)
print()
new_list = []

for i in range(len(data)):
    payload = {
        'affiliate': data[i].get('affiliate'),
        'webmaster': data[i].get('webmaster'),
        'registrations': 0,
        'loans': 0,
        'revenue': 0
    }
    if payload not in new_list:
        new_list.append(payload)

for i in new_list:
    print(i)
print()

for i in range(len(data)):
    for j in range(len(new_list)):
        if data[i].get('affiliate') == new_list[j].get('affiliate') and data[i].get('webmaster') == new_list[j].get('webmaster'):
            new_list[j]['registrations'] += data[i]['registrations']
            new_list[j]['loans'] += data[i]['loans']
            new_list[j]['revenue'] += data[i]['revenue']


for i in new_list:
    print(i)
