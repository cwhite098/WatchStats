import pandas as pd
import numpy as np

# Read the data and remove unnecessary cols
df = pd.read_csv('NMC-60-abridged.csv')
df = df[['stateabb', 'year', 'milper']]
df.set_index('year')

# Create output df
df1 = pd.DataFrame()
df1['year'] = np.linspace(1816, 2016, 201, dtype=np.int)
df1.set_index('year', inplace=True, drop=True)

# Loop through each country
states = df['stateabb'].unique()
for state in states:

    # Get time series of army size for each country
    state_df = df[df['stateabb']==state]
    state_df = state_df[['year', 'milper']]
    state_df.set_index('year', inplace=True, drop=True)

    # Add each country's data to output df
    df1 = pd.concat((df1, state_df), axis=1)
    df1.columns = [*df1.columns[:-1], state]

# Fill the missing values with 0s
df1 = df1.fillna(0)

# Find the top 10 countries for each year so only the necessary ones are collected
top_countries = []
for year in df1.index:

    # Isolate the data for each year
    year_data = df1.loc[[year]]
    year_data = list(year_data.iloc[0,:])

    # Sort by largest army
    cols = np.argsort(year_data)

    # Add to top countries list and remove duplicates
    top_countries += list(df1.columns[cols[-10:]])
    top_countries = list(set(top_countries))

df1 = df1[top_countries]

# Remove missing values and interpolate
df1 = df1.replace(-9, np.nan)
df1 = df1.interpolate()
# Fill in any remaining nans with 0
df1 = df1.fillna(0)

df1.to_csv('states.csv')