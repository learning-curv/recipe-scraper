from __future__ import annotations
from abc import ABC, abstractmethod
from scraper import Scraper
from the_chunky_chef_scraper import TheChunkyChefScraper


class ScraperFactory(ABC):
    def create(self):
      pass


class TheChunkyChefScraperFactory(ScraperFactory):
    def create(self) -> Scraper:
        return TheChunkyChefScraper()
