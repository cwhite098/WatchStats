import os
import pandas as pd


def get_tickers(path):
    '''
    Get list of files -> read them -> add ticker to list -> make ticker : name dict
    '''
    tickers = []
    name_dict = {}
    for file in os.listdir(path):

        # Read the data from the files
        df = pd.read_csv(path+file, delimiter = "\t")
        tickers += list(df['Symbol'])

        # Get the name of the company
        for i in range(df.shape[0]):
            row = df.iloc[i,:]
            name_dict[row['Symbol']] = row['Description']

    return tickers, name_dict



def main():
    tickers, name_dict = get_tickers('symbols/')
    print('Number of tickers: ', len(tickers))
    print('Number of names in dict: ', len(name_dict))


if __name__ == '__main__':
    main()