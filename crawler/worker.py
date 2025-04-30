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
from itertools import islice

import os
import json


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self._uniquePages = 0
        self._successfulPages = 0
        self._longestPageLength = 0
        self._longestPageUrl = ''
        self._wordCounter = {}
        self._domains = {}

        self._stopwords = set(stopwords.words('english')) # store stopwords

        self._load_stats() # check if we have a previous save

        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        while 1: 
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
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
            self._uniquePages += 1
            
            scraped_urls = scraper.scraper(tbd_url, resp, soup)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)

    def _load_stats(self):
         if not os.path.exists('./Logs/statistics.json'):
            return
         else:
            self.logger.info('stats save found')
            with open('./Logs/statistics.json', 'r') as file:
                data = json.load(file)

            self._uniquePages = data['uniquePages']
            self._successfulPages = data['successfulPages']
            self._longestPageLength = data['longestPageLength']
            self._longestPageUrl = data['longestPageUrl']
            self._wordCounter = data['wordCounter']
            self._domains = data['domains']


    def _save_stats(self):
        data = {}
        data['uniquePages'] = self._uniquePages
        data['successfulPages'] = self._successfulPages
        data['longestPageLength'] = self._longestPageLength
        data['longestPageUrl'] = self._longestPageUrl
        data['wordCounter'] = self._wordCounter
        data['domains'] = self._domains
        with open('./Logs/statistics.json', 'w') as file:
            file.write(json.dumps(data))

        self.logger.info('saved stats to file')
            

    '''
    updates the statistics for the worker
    and updates the worker log with the information

    '''
    def _update_statistics(self, tbd_url, resp, soup):
        tokenizer = RegexpTokenizer(r'\b[a-zA-Z]+\'?\w*\b') # written while referencing https://www.w3schools.com/python/python_regex.asp
        pageLen = 0
        for word in tokenizer.tokenize(soup.get_text()):
            word = word.lower()
            if word not in self._stopwords and len(word) != 1:
                pageLen += 1
                if word in self._wordCounter:
                    self._wordCounter[word] += 1
                else:
                    self._wordCounter[word] = 1

        if pageLen > self._longestPageLength:
            self._longestPageLength = pageLen
            self._longestPageUrl = tbd_url
            self.logger.info(f"Page {tbd_url}, new longest page with length <{pageLen}>.")

        self._successfulPages += 1

        parsed = urlparse(tbd_url)
        if parsed.netloc not in self._domains:
            self._domains[parsed.netloc] = 1
        else:
            self._domains[parsed.netloc] += 1

        if self._successfulPages % 50 == 0: 
            self._save_stats()

    

    def _final_report(self):
        self._save_stats()
        self.logger.info(f"Page {self._longestPageUrl}, longest page with length <{self._longestPageLength}>.")
        #self.logger.info("WordCounts:")
        #sortedDict = sorted(self._wordCounter.items(), key = lambda current:current[1], reverse=True)
        #for first, second in sortedDict:
        #    self.logger.info(f" - {first}: {second}")
        self.logger.info(f"Unique pages: {self._uniquePages}.")
        self.logger.info("Domains:")
        for first, second in sorted(self._domains.items()):
            self.logger.info(f" - {first}: {second}")



