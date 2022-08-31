import pandas as pd

df = pd.read_csv('out.csv')
df['date'] = df['Unnamed: 0']
df = df.drop('Unnamed: 0', axis=1)
df['date'] = pd.DatetimeIndex(df['date'])

original_dates = df['date']

df = df.set_index('date')

cols = df.columns

df = df.groupby(pd.Grouper(freq='1Y'))

df_yearly = pd.DataFrame(columns=cols)

indices = []
for group in df:
    # Each group is a tuple: (year, df)
    year = group[0]
    year_df = group[1]

    year_df = year_df.fillna(0)

    sales = pd.DataFrame(columns=cols)
    for artist in year_df.columns:
        artist_col = year_df[artist]
        artist_yearly_sales = artist_col.iloc[-1] - artist_col.iloc[0]
        sales[artist] = [artist_yearly_sales]
    
    indices.append(year)
    
    df_yearly = df_yearly.append(sales)

# resample the original dates and add as index column to new df
new_index = pd.DatetimeIndex(indices)
print(df_yearly.shape)
print(new_index.shape)

df_yearly.index = new_index
df_yearly.to_csv('yearly_sales.csv')

print(1)