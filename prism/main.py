import pandas as pd
from prism.prisp_script import *
import jinja2

data = pd.read_csv('data.csv')

result = get_final_data_table(data=data, group_by='date')
print(result)
