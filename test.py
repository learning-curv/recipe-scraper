from __future__ import annotations
from scraper_factory import createScraperFactory, FactoryType
from abc import ABC, abstractmethod, abstractproperty


if __name__ == "__main__":
    print("App: Launched")
    factory = createScraperFactory(FactoryType.THE_CHUNKY_CHEF)
    scraper = factory.create()
    scraper.get_recipes()
    scraper.process_recipes(
        scraper.get_description,
        scraper.get_author,
        scraper.get_servings,
        scraper.get_prep_time,
        scraper.get_cook_time,
        scraper.get_ingredient_groups,
        scraper.get_instruction_groups,
    )

    scraper.show_recipes()
