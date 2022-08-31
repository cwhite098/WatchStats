from typing import final
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
import time
from get_artists import get_artists
import pandas as pd
import numpy as np
from tqdm import tqdm
from final_formatting import final_formatting

def get_artist_data(artist):

    albums_url = 'https://www.riaa.com/gold-platinum/?tab_active=default-award&ar='+artist+'&ti=&lab=&genre=&format=Album&date_option=release&from=&to=&award=&type=&category=&adv=SEARCH#search_section'
    singles_url = 'https://www.riaa.com/gold-platinum/?tab_active=default-award&ar='+artist+'&ti=&lab=&genre=&format=Single&date_option=release&from=&to=&award=&type=&category=&adv=SEARCH#search_section'

    urls = [albums_url, singles_url]

    out_dfs = []
    for url in urls:

        driver = webdriver.Chrome()
        driver.get(url)

        while True:
            # look for load more button, click if found, break if not
            try:
                next_link = driver.find_element_by_class_name('link-arrow-gnp')
            except:
                print('reached page bottom')
                break
            try:
                next_link.click()
                print('next page')
            except ElementNotInteractableException:
                print('reached bottom')
                break
            except ElementClickInterceptedException:
                print('reached bottom')
                break

        # Click all the 'MORE DETAILS' links
        driver.maximize_window() # for some reason you must do this
        show_more_links = driver.find_elements_by_link_text('MORE DETAILS')
        for more_details in show_more_links:
            time.sleep(0.7)
            more_details.click()
            time.sleep(0.5)

        # Get the html data from the full list of albums/singles
        driver.execute_script("window.scrollTo(0, 1080)") 
        soup = BeautifulSoup(driver.page_source)

        # Get the album names
        rows = soup.find_all('tr', class_=['table_award_row expanded','table_award_row expanded hasContent'])
        names = []
        total_data = []
        for row in rows:
            contents = row.contents
            album = contents[5].contents[0]
            if album == 'ALBUM' or album =='SINGLE':
                album = contents[2].contents[0]
            names.append(album)

        # Get the data from the row
        rows = soup.find_all('div', class_='row more_detail_div')
        for row in rows:
            album_data = []
            table = row.find_all('tr', class_='content_recent_table')

            for award in table:
                data = award.contents[1].contents[0] # gets the award and date in some string
                data = data.split()

                award = str(data[0]) # need to parse this to a number
                date = data[-3] + ' ' + data[-2] + ' ' + data[-1] # reconstruct date

                # Parse the award
                if award == 'Gold':
                    sales = 500000
                elif award == 'Platinum':
                    sales = 1000000
                elif award == 'Diamond':
                    sales = 10000000
                else:
                    sales = int(award[:-1]) * 1000000

                album_data.append([date, sales])

            total_data.append(album_data)

        driver.quit()
        
        print(len(total_data))
        print(len(names))
        if not len(names) == len(total_data):
            raise ValueError('Name data mismatch!')

        # Make a dataframe using the scraped data
        total_df = pd.DataFrame(columns=['date'])
        total_df['date'] = pd.to_datetime(total_df['date'], infer_datetime_format=True)
        total_df.set_index('date', inplace=True, drop=True)

        for i, album in enumerate(total_data):

            name = names[i]
            df1 = pd.DataFrame(album)
            df1.columns = ['date', name]
            df1['date'] = pd.to_datetime(df1['date'], infer_datetime_format=True)
            df1 = df1.drop_duplicates(['date'])
            df1.set_index('date', inplace=True, drop=True)
            total_df = pd.concat((total_df,df1), axis=1)

        out_dfs.append(total_df)

    out_df = pd.concat(out_dfs, axis=1)
    out_df = out_df.interpolate()

    out_df['total'] = out_df.sum(axis=1) # get totals

    return out_df



def main():
    print('Getting artists...')
    artists, names = get_artists()

    names = []
    for art in artists:
        art.upper()
        art = art.replace('+', ' ')
        names.append(art)

    totals = pd.DataFrame()

    print('Scraping data...')
    for artist in tqdm(artists):
        print(artist)
        artist_data = get_artist_data(artist)

        artist_df = artist_data['total']
        totals = pd.concat((totals,artist_df), axis=1)

    totals.columns = names
    totals = totals.interpolate()
    print(totals.head)
    totals.to_csv('preformat.csv')
    # find first row with 10 entries and make that the first in the df
    totals = final_formatting(totals)
    totals.to_csv('out.csv')




if __name__ == '__main__':
    main()


    