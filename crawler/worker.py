from threading import Thread
from enum import Enum
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
import nltk
from nltk.corpus import stopwords # used geeksforgeeks.com tutorial for removing stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self._uniquePages = 0
        self._longestPageLength = 0
        self._longestPageUrl = ''
        self._stopwords = set(stopwords.words('english')) # store stopwords
        self._wordCounter = {}
        self._domains = set()

        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while 1: 
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url or self._uniquePages > 100:# change later, just setting a testing limit
                self.logger.info("Frontier is empty. Stopping Crawler.")
                self._final_report()
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")

            if(resp.status == 200):
                soup = BeautifulSoup(resp.raw_response.content, 'lxml')
                self._update_statistics(tbd_url, resp, soup)
            else:
                soup = None
            
            scraped_urls = scraper.scraper(tbd_url, resp, soup)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)


    '''
    updates the statistics for the worker
    and updates the worker log with the information

    '''
    def _update_statistics(self, tbd_url, resp, soup):
        tokenizer = RegexpTokenizer(r'\b[a-zA-Z]+\'?\w*\b') # written while referencing https://www.w3schools.com/python/python_regex.asp
        pageLen = 0
        for word in tokenizer.tokenize(soup.get_text()):
            word = word.lower()
            if word not in self._stopwords:
                pageLen += 1
                if word in self._wordCounter:
                    self._wordCounter[word] += 1
                else:
                    self._wordCounter[word] = 1

        if pageLen > self._longestPageLength:
            self._longestPageLength = pageLen
            self._longestPageUrl = tbd_url
            self.logger.info(f"Page {tbd_url}, new longest page with length <{pageLen}>.")

        self._uniquePages += 1


    def _final_report(self):
        self.logger.info(f"Page {self._longestPageUrl}, longest page with length <{self._longestPageLength}>.")
        self.logger.info("WordCounts:")
        sortedDict = sorted(self._wordCounter.items(), key = lambda current:current[1], reverse=True)
        for first, second in sortedDict:
            self.logger.info(f" - {first}: {second}")
        self.logger.info(f"Unique pages: {self._uniquePages}.")
        self.logger.info("Domains:")
        for current in self._domains:
            self.logger.info(f" - {current}")



