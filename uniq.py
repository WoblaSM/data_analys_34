import pandas as pd
import random
df = pd.read_csv('Данные по использованию климатических систем.csv', delimiter=';', skipinitialspace=True, decimal=',')
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()
print(df['утепление'].unique())