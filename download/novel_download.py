#!/usr/bin/env python3.11

# system
import time
import random
import argparse

# web
from bs4 import BeautifulSoup
import cloudscraper


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='chapter url', type=str, required=True)
    parser.add_argument('-l', '--limit', help='number of chapters to download', type=int, default=3)
    parser.add_argument('-w', '--wait', help='wait before each request in milliseconds (minimum time)', type=int, default=500)
    parser.add_argument('-c', '--counter', help='counter is prepended to downloaded file for consistency', type=int, default=0)
    args = parser.parse_args()

    # setup
    url = args.url
    limit = args.limit
    wait = args.wait

    # find all chapters
    scraper = cloudscraper.create_scraper()
    while limit > 0:
        # counter
        counter = args.limit - limit + 1 + args.counter

        # download page
        print(f'[ html2pdf ] ({counter}) Downloading page content: <{url}>')
        page = scraper.get(url).text

        # parse html
        print(f'[ html2pdf ] Parsing HTML...')
        soup = BeautifulSoup(page, "html.parser")
        title = soup.title.string
        
        # find chapter navigation
        print(f'[ html2pdf ] Looking for chapter nagivation section...')
        result = soup.find_all('div', class_='chapter-nav')
        if not len(result):
            print(f'[ html2pdf ] error')
            break

        # find chapter links
        print(f'[ html2pdf ] Extracting chapter URLs...')
        result = result[0].find_all('a')
        if not len(result):
            print(f'[ html2pdf ] error')
            break
        
        # select url to next chapter
        print(f'[ html2pdf ] Selecting URL to next chapter...')
        next_url = None
        for href in result:
            if href['class'][0] == 'next':
                next_url = href['href']
                break
                
        # save html
        print(f'[ html2pdf ] Saving to <({counter}) {title}.html>')
        with open(f'({counter}) {title}.html', 'w') as f: 
            f.write(page)

        # set url
        url = next_url
        if not url:
           print(f'[ html2pdf ] invalid next url: <{next_url}>!')
           break

        # update downloaded chapters
        limit -= 1

        # wait (random time)
        time.sleep((wait * (random.random() + 3)) / 1000)
    



