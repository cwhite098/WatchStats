from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


def get_artists():

    url1 = 'https://www.riaa.com/gold-platinum/?advance_search=1&tab_active=awards_by_artist&format_option=album-ep#search_section'
    url2 = 'https://www.riaa.com/gold-platinum/?advance_search=1&tab_active=awards_by_artist&format_option=singles#search_section'
    urls = [url1, url2]
    
    biggest_artists = []
    names = []
    for url in urls:
        driver = webdriver.Chrome()
        driver.get(url)
        for i in range(3):
            # look for load more button, click if found, break if not
            try:
                next_link = driver.find_element_by_class_name('link-arrow-gnp')
                ActionChains(driver).move_to_element(next_link).perform()
                time.sleep(0.5)
                next_link.click()
            except:
                print('reached page bottom')
                break
        soup = BeautifulSoup(driver.page_source, features="html.parser")

        artists = soup.find_all('h2', class_='artist')
        driver.quit()

        
        for artist in artists:
            name = artist.contents[0]

            # reformate for putting in url
            name1 = name.lower()
            name1 = name1.replace(' ', '+')

            biggest_artists.append(name1)
            names.append(name)

    # Remove duplicates
    biggest_artists = list(set(biggest_artists))

    print('Number of artists: ', len(biggest_artists))
    return biggest_artists, names


def main():
    artists = get_artists()
    print(len(artists))


if __name__ == '__main__':
    main()
