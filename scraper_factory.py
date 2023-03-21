from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from scraper import Scraper
from the_chunky_chef_scraper import TheChunkyChefScraper


def createScraperFactory(factoryType):
    return _scrapers[factoryType]


class ScraperFactory(ABC):
    def create(self):
        pass


class TheChunkyChefScraperFactory(ScraperFactory):
    def create(self) -> Scraper:
        return TheChunkyChefScraper()


class FactoryType(Enum):
    THE_CHUNKY_CHEF = "the_chunky_chef"


_scrapers = {
    FactoryType.THE_CHUNKY_CHEF: TheChunkyChefScraperFactory(),
}
