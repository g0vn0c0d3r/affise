import pandas as pd
from prism.prisp_script import *

data = pd.read_csv('data.csv')

result = get_final_data_table(data=data, group_by='state, city, date')
print(result)
