from cmath import nan
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

# Fill the missing values with 0s
df1 = df.fillna(0)
def get_top_n(df, n):
    # Find the top 10 countries for each year so only the necessary ones are collected
    top_countries = []
    for year in df.index:

        # Isolate the data for each year
        year_data = df.loc[[year]]
        year_data = list(year_data.iloc[0,:])

        # Sort by largest army
        cols = np.argsort(year_data)

        # Add to top countries list and remove duplicates
        top_countries += list(df.columns[cols[-n:]])
        top_countries = list(set(top_countries))

    return top_countries

top_countries = get_top_n(df1, 20)
df1 = df1[top_countries]
df1.index = df1['Unnamed: 0']
df1 = df1.drop('Unnamed: 0', axis=1)
df1.to_csv('out.csv')

df = pd.read_csv('extra_data.csv')
df = df.fillna(0)
df = df.transpose()
df.columns = df.iloc[0]
df = df.iloc[1:,:]
df = df.loc[['2017','2018','2019']]
top_countries = get_top_n(df, 20)
df = df[top_countries]
df.to_csv('extra_formatted.csv')

df1.index = pd.DatetimeIndex(df1.index)
df.index = pd.DatetimeIndex(df.index)

total_df = pd.concat([df1, df])
total_df.to_csv('total.csv')

print('test')