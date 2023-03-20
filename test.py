from __future__ import annotations
from scraper_factory import TheChunkyChefScraperFactory
from abc import ABC, abstractmethod, abstractproperty


class Animal(ABC):
    @abstractmethod
    def foo(self):
        pass

    def speak(self):
        print("oink")


class Pig(Animal):
    def foo(self):
        print("hello")


if __name__ == "__main__":
    print("App: Launched")
    factory = TheChunkyChefScraperFactory()
    scraper = factory.create()
    scraper.get_recipes()
    scraper.process_recipes(
        scraper.get_description,
        scraper.get_author,
        scraper.get_servings,
        scraper.get_prep_time,
        scraper.get_cook_time,
    )
