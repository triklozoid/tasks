import re
import os

from datetime import datetime
from getwallpapers import build_url, getwallpapers, WALLPAPERS_PATH

FILES_LIST = (
    'jan-17-a-new-start-nocal-640x480.jpg',
    'jan-17-colorful-2017-nocal-640x480.png',
    'jan-17-hello-summer-in-australia-nocal-640x480.png',
    'jan-17-love-makes-you-warm-nocal-640x480.png',
    'jan-17-reindeer-nocal-640x480.png',
    'jan-18-big-things-often-have-small-beginnings-cal-640x480.png',
    'jan-18-big-things-often-have-small-beginnings-nocal-640x480.png',
    'jan-18-cheers-to-new-challenges-cal-640x480.png',
    'jan-18-cheers-to-new-challenges-nocal-640x480.png',
    'jan-18-colours-of-festivity-and-celebration-cal-640x480.png',
    'jan-18-colours-of-festivity-and-celebration-nocal-640x480.png',
    'jan-18-every-new-year-gives-you-a-good-place-to-start-over-cal-640x480.png',
    'jan-18-every-new-year-gives-you-a-good-place-to-start-over-nocal-640x480.png',
    'jan-18-january-is-the-month-for-dreaming-cal-640x480.png',
    'jan-18-january-is-the-month-for-dreaming-nocal-640x480.png',
    'jan-18-new-year-a-new-beginning-cal-640x480.jpg',
    'jan-18-new-year-a-new-beginning-nocal-640x480.jpg',
    'jan-18-open-the-doors-of-the-new-year-cal-640x480.jpg',
    'jan-18-open-the-doors-of-the-new-year-nocal-640x480.jpg',
    'jan-18-wishing-a-coloufull-joyfull-year-ahead-cal-640x480.png',
    'jan-18-wishing-a-coloufull-joyfull-year-ahead-nocal-640x480.png',
)


def test_build_url():
    date = datetime.strptime('012018', '%m%Y')
    url = build_url(date)
    assert url == 'https://www.smashingmagazine.com/2017/12/desktop-wallpaper-calendars-january-2018/', url


def test_getwallpapers(requests_mock):
    date = datetime.strptime('012018', '%m%Y')
    url = build_url(date)
    with open('fixtures/list.html') as f:
        requests_mock.get(url, text=f.read())
    matcher = re.compile('http://files.smashingmagazine.com')
    requests_mock.get(matcher, text='img_body')
    getwallpapers(date, '640x480')
    for file_name in FILES_LIST:
        path = '{}/{}'.format(WALLPAPERS_PATH, file_name)
        assert os.path.exists(path)
