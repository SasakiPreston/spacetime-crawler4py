import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse



def matches(s):
    return re.search(r"\d{4}-\d{2}", s)


if __name__ == '__main__':
    url = 'https://ics.uci.edu/~cs224/'
    #parsed = urlparse(url)
    #print(parsed.netloc)
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    for current in soup.get_text():
        print(current)
    #tags = soup.find_all('a')
    #for current in tags:
    #    if 'href' in current.attrs:
    #        print(current.attrs['href'])

    #print('https://ics.uci.edu/events/month/2028-05/ matches: ' + str(matches('https://ics.uci.edu/events/month/2028-05/')))
    #print('https://ics.uci.edu/events/2025-04-29/ matches: ' + str(matches('https://ics.uci.edu/events/2025-04-29/')))
    #print('https://ics.uci.edu/events/list/?tribe-bar-date=2025-05-05&eventDisplay=past matches: ' + str(matches('https://ics.uci.edu/events/list/?tribe-bar-date=2025-05-05&eventDisplay=past')))

    #stop = set(stopwords.words('english'))
    #tokenizer = RegexpTokenizer(r'\b[a-zA-Z]+\'?\w*\b')
    '''words = []
    l = "mumei\'s graduation was yesterday, very sad and I'm sad 200 percent's"
    for word in tokenizer.tokenize(l):#soup.get_text()):
    #for word in word_tokenize(l):
        word = word.lower()
        if word not in stop:
            words.append(word)
    for current in words:
        print(current)
    '''