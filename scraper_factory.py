from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from scraper import Scraper
from the_chunky_chef_scraper import TheChunkyChefScraper
from bon_appetit_scraper import BonAppetitScraper


def createScraperFactory(factoryType):
    return _scrapers[factoryType]


class ScraperFactory(ABC):
    def create(self):
        pass


class TheChunkyChefScraperFactory(ScraperFactory):
    def create(self) -> Scraper:
        return TheChunkyChefScraper()


class BonAppetitFactory(ScraperFactory):
    def create(self) -> Scraper:
        return BonAppetitScraper()


class ScraperType(Enum):
    THE_CHUNKY_CHEF = "the_chunky_chef"
    BON_APPETIT = "bon_appetit"


_scrapers = {
    ScraperType.THE_CHUNKY_CHEF: TheChunkyChefScraperFactory(),
    ScraperType.BON_APPETIT: BonAppetitFactory(),
}
