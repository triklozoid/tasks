#!/usr/bin/env python3

import os
import argparse
import requests

from datetime import datetime, timedelta
from parsel import Selector
from urllib.parse import urlparse

RESOLUTIONS = ('320x480', '640x480')
WALLPAPERS_PATH = 'wallpapers'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help='Wallpapers date in MMYYYY format, e.g. "082018"')
    parser.add_argument("resolution", help='Wallpaper resolution, available: {}'.format(', '.join(RESOLUTIONS)))
    args = parser.parse_args()

    date = datetime.strptime(args.date, '%m%Y')
    previous_month_date = date - timedelta(days=1)
    print(date.strftime('%B').lower())

    url = 'https://www.smashingmagazine.com/{}/{:01}/desktop-wallpaper-calendars-{}-{}/'.format(
        previous_month_date.year,
        previous_month_date.month,
        date.strftime('%B').lower(),
        date.year
    )

    if not os.path.exists(WALLPAPERS_PATH):
        os.makedirs(WALLPAPERS_PATH)

    r = requests.get(url)
    print(r.text)
    sel = Selector(text=r.text)
    print(sel)
    for l in sel.css('#article__content > div > ul > li > a'):
        element_resolution = l.css('::text').get()

        if element_resolution == args.resolution:
            print(l.attrib['href'])
            img_url = l.attrib['href']

            file_path = '{}/{}'.format(WALLPAPERS_PATH, urlparse(img_url).path.split('/')[-1])
            response = requests.get(img_url)

            with open(file_path, 'wb') as f:
                f.write(response.content)

if __name__ == '__main__':
    main()
