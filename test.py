import requests
from bs4 import BeautifulSoup
import re

def matches(s):
    return re.search(r"\d{4}-\d{2}", s)


if __name__ == '__main__':
    '''url = 'https://ics.uci.edu/~mbdillen/compsci161/'
    tags = BeautifulSoup(requests.get(url).text, 'lxml').find_all('a')
    for current in tags:
        if 'href' in current.attrs:
            print(current.attrs['href'])'''

    print('https://ics.uci.edu/events/month/2028-05/ matches: ' + str(matches('https://ics.uci.edu/events/month/2028-05/')))
    print('https://ics.uci.edu/events/2025-04-29/ matches: ' + str(matches('https://ics.uci.edu/events/2025-04-29/')))
    print('https://ics.uci.edu/events/list/?tribe-bar-date=2025-05-05&eventDisplay=past matches: ' + str(matches('https://ics.uci.edu/events/list/?tribe-bar-date=2025-05-05&eventDisplay=past')))