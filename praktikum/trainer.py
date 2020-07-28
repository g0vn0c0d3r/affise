import pandas as pd
import numpy
import matplotlib.pyplot as plt

raw_data = pd.read_csv('real_estate_data.csv', sep='\t')
data = raw_data

data['ceiling_height'].fillna(value=data['ceiling_height'].median(), inplace=True)



print(data.isna().sum())


