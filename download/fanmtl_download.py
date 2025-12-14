#!/usr/bin/env python3.11

# system
import os
import time
import random
import argparse
from urllib.parse import urljoin

# web
from bs4 import BeautifulSoup
import cloudscraper


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='chapter url', type=str, required=True)
    parser.add_argument('-l', '--limit', help='number of chapters to download', type=int, default=3)
    parser.add_argument('-w', '--wait', help='wait before each request in milliseconds (minimum time)', type=int, default=500)
    parser.add_argument('-c', '--counter', help='counter is prepended to downloaded file for consistency', type=int, default=0)
    parser.add_argument('-s', '--save-folder', help='download folder', type=str, default='download')
    args = parser.parse_args()

    # setup
    url = args.url
    limit = args.limit
    wait = args.wait
    save_folder = args.save_folder
    filename_max = 30

    # ensure folder exists
    os.makedirs(save_folder, exist_ok=True)

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
        result = soup.find_all('div', class_='chapternav skiptranslate notranslate')
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
            if href['class'][0] == 'nextchap':
                next_url = urljoin(url, href['href']) # convert relative URL to absolute URL
                break
                
        # save html
        filename = f'({counter}) {title if len(title) < filename_max else title[:filename_max]}....html' 
        print(f'[ html2pdf ] Saving to <({counter}) {filename}>')
        with open(os.path.join(save_folder, filename), 'w') as f: 
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
    



