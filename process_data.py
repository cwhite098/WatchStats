import os
import pandas as pd
import numpy as np

files = os.listdir('fortune500/csv')

# Get the data for required companies
output_df = pd.DataFrame()
for file in files:
    df = pd.read_csv('fortune500/csv/' + file)

    # Get top 10 each year and reformat
    top10 = df.iloc[:10,:]
    top10 = top10[['company','revenue ($ millions)']]
    top10 = top10.transpose()
    top10.columns = top10.iloc[0]
    top10 = top10.iloc[1,:]

    # Add new row to output
    output_df = output_df.append(top10)

# add data for 2020 and 2021
new_data1 = pd.DataFrame(columns=['Walmart', 'Amazon.com', 'Exxon Mobil', 'Apple', 'CVS Health', 
                'Berkshire Hathaway', 'UnitedHealth Group', 'McKesson', 'AT&T', 'AmerisourceBergen'],
                data = [[523964, 280522, 264938, 260174, 256776, 254616, 242155, 214319, 181193, 179589]])

new_data2 = pd.DataFrame(columns=['Walmart', 'Amazon.com', 'Apple', 'CVS Health', 'UnitedHealth Group',
                'Berkshire Hathaway' , 'McKesson', 'AmerisourceBergen', 'Alphabet', 'Exxon Mobil'],
                data = [[559151, 386064, 274515, 268706, 257141, 245510, 231051, 189893, 182527, 181502]])

new_data3 = pd.DataFrame(columns=['Walmart', 'Amazon.com', 'Apple', 'CVS Health', 'UnitedHealth Group',
                'Exxon Mobil', 'Berkshire Hathaway', 'Alphabet', 'McKesson', 'Costco Wholesale'],
                data = [[572754, 469822, 378323, 292111, 287597, 276692, 276094, 257637, 257006, 210219]])

output_df = output_df.append(new_data1)
output_df = output_df.append(new_data2)
output_df = output_df.append(new_data3)

# Set index as the year
output_df.index = np.linspace(1955, 2022, 68, dtype=np.int)

print(output_df.head())
output_df.to_csv('top10_each_year.csv')