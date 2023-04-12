from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
import json

from postgres_interface import save_recipes
from logging_config import logger


def get_text(html):
    return html.text if html else None


def _process_recipe(recipe, *operators):
    recipe_obj, recipe_raw = recipe

    if not recipe_raw:
        return None

    for operator in operators:
        try:
            recipe_obj.update(operator(recipe_raw))
        except AttributeError:
            logger.error({"operator": operator, "recipe": recipe_obj})

    return recipe_obj


class Scraper(ABC):
    def __init__(self):
        self.raw_recipes = []
        self.recipes = []

    @abstractproperty
    def url(self):
        return None

    @abstractmethod
    def get_recipes(self, page_index):
        pass

    @abstractmethod
    def process_recipes(self, *operators):
        pass

    @abstractmethod
    def get_description(self, recipe):
        pass

    @abstractmethod
    def get_author(self, recipe):
        pass

    @abstractmethod
    def get_image_link(self, recipe):
        pass

    @abstractmethod
    def get_servings(self, recipe):
        pass

    @abstractmethod
    def get_prep_time(self, recipe):
        pass

    @abstractmethod
    def get_cook_time(self, recipe):
        pass

    @abstractmethod
    def get_ingredient_groups(self, recipe):
        pass

    @abstractmethod
    def get_instruction_groups(self, recipe):
        pass

    @abstractmethod
    def should_continue(self):
        pass

    def process_recipes(self, *operators):
        list(
            map(
                lambda recipe: _process_recipe(recipe, *operators),
                zip(self.recipes, self.raw_recipes),
            )
        )

    def scrape(self, start_index):
        page_index = start_index

        while self.should_continue(page_index):
            logger.info(f"scraping page: {page_index}")
            self.get_recipes(page_index)
            self.process_recipes(
                self.get_description,
                self.get_author,
                self.get_image_link,
                self.get_servings,
                self.get_prep_time,
                self.get_cook_time,
                self.get_ingredient_groups,
                self.get_instruction_groups,
            )

            logger.info("Writing to database")
            self.save_recipes()
            page_index += 1

    def show_recipes(self):
        print(json.dumps(self.recipes, indent=2))

    def save_recipes(self):
        save_recipes(self.recipes)
