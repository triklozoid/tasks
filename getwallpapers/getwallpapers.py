#!/usr/bin/env python3

import os
import sys
import argparse
import requests

from datetime import datetime, timedelta
from parsel import Selector
from urllib.parse import urlparse
from requests.exceptions import RequestException

RESOLUTIONS = ('320x480', '640x1136', '640x480', '750x1334', '800x450',
               '800x480', '800x600', '1024x1024', '1024x768', '1152x864',
               '1242x2208', '1280x1024', '1280x720', '1280x800', '1280x960',
               '1366x768', '1400x1050', '1440x810', '1440x900', '1600x1200',
               '1600x900', '1680x1050', '1680x1200', '1680x1260', '1680x945',
               '1920x1080', '1920x1200', '1920x1440', '2560x1440', '2880x1800',
               '3840x2160')
WALLPAPERS_PATH = 'wallpapers'
BASE_URL = 'https://www.smashingmagazine.com/{}/{:02}/desktop-wallpaper-calendars-{}-{}/'


def validate_date(value):
    try:
        datetime.strptime(value, '%m%Y')
    except ValueError:
        raise argparse.ArgumentTypeError(
            'Invalid date value: "{}"'.format(value))
    return value


def validate_resolution(value):
    if value not in RESOLUTIONS:
        raise argparse.ArgumentTypeError(
            'Invalid resolution: "{}", must be one of {}'.format(
                value, ', '.join(RESOLUTIONS)))
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "date",
        help='Wallpapers date in MMYYYY format, e.g. "082018"',
        type=validate_date)
    parser.add_argument(
        "resolution",
        help='Wallpaper resolution, available: {}'.format(
            ', '.join(RESOLUTIONS)),
        type=validate_resolution)
    args = parser.parse_args()

    date = datetime.strptime(args.date, '%m%Y')
    previous_month_date = date - timedelta(days=1)

    url = BASE_URL.format(previous_month_date.year, previous_month_date.month,
                          date.strftime('%B').lower(), date.year)

    if not os.path.exists(WALLPAPERS_PATH):
        os.makedirs(WALLPAPERS_PATH)

    response = requests.get(url)
    if response.status_code == 404:
        print('Can not find wallpapers page for date {}'.format(args.date))
        sys.exit(1)
    if response.status_code != 200:
        print('Unknown error loading wallpapers list {}'.format(args.date))
        sys.exit(1)

    sel = Selector(text=response.text)
    for element in sel.css('#article__content > div > ul > li > a'):
        element_resolution = element.css('::text').get()

        if element_resolution == args.resolution:
            img_url = element.attrib['href']
            file_path = '{}/{}'.format(WALLPAPERS_PATH,
                                       urlparse(img_url).path.split('/')[-1])
            print('Try download {} ...'.format(file_path), end='', flush=True)
            try:
                response = requests.get(img_url)
            except RequestException:
                print('error')
                continue
            else:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print('ok')


if __name__ == '__main__':
    main()
