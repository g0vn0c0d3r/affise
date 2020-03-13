import json


a = json.load(open('offer15.json'))

for click in a['clicks']:
	print(click)
