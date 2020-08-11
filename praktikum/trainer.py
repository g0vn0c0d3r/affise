import pandas as pd


calls = pd.read_csv('project_3/calls.csv')
calls['duration'] = calls['duration'] * 60
# calls['duration'] = calls['duration'] * 60
# print(calls.query('duration > 0').groupby(by='user_id')['duration'].median())
