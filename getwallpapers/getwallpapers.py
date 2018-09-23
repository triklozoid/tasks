#!/usr/bin/env python3

import argparse
import requests

from datetime import datetime, timedelta

RESOLUTIONS = ('320x480', '640x480')

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

    print(url)


    


    print('test')

if __name__ == '__main__':
    main()
