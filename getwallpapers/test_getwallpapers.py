import re

from datetime import datetime
from getwallpapers import build_url, getwallpapers


def test_build_url():
    date = datetime.strptime('012018', '%m%Y')
    url = build_url(date)
    assert url == 'https://www.smashingmagazine.com/2017/12/desktop-wallpaper-calendars-january-2018/', url


def test_getwallpapers(requests_mock):
    date = datetime.strptime('022016', '%m%Y')
    url = build_url(date)
    with open('fixtures/list.html') as f:
        requests_mock.get(url, text=f.read())
    matcher = re.compile('http://files.smashingmagazine.com')
    requests_mock.get(matcher, text='img_body')
    getwallpapers(date, '640x480')
