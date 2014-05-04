"""
Scrape from bestforpuzzles.com the clues of cryptic crossword puzzles.
"""


import urllib2
import datetime

import BeautifulSoup
import re

web_page = "http://bestforpuzzles.com/daily-cryptic/puzzles/"

inc = datetime.timedelta(days=1)


def make_date_string(date):
    first = date.strftime("%Y-%m")
    second = date.strftime("%Y-%m-%d")
    url = "%s%s/dc1-%s.html" % (web_page, first, second)
    return url


date = datetime.date.today()
for i in range(0, 60):
    name = "%s.txt" % date.strftime("%Y-%m-%d")
    f = open(name, "w")
    page = urllib2.urlopen(make_date_string(date))

    soup = BeautifulSoup.BeautifulSoup(page.read())
    tables = soup.findChildren('table')
    t = tables[1]
    rows = t.findChildren(['tr'])
    row = rows[0]
    text = str(row)

    m = re.findall('</b>[^<]*<br />', text)
    final = []
    for match in m:
        final.append(match[4:-6].replace('\n', ""))

    for clue in final:
        f.write(clue + "\n")

    f.close()
    date -= inc


