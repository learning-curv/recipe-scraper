from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
import json

from postgres_interface import save_recipes


def get_text(html):
    return html.text if html else None


def _process_recipe(recipe, *operators):
    recipe_obj, recipe_raw = recipe

    if not recipe_raw:
        # print(recipe)
        return None

    for operator in operators:
        recipe_obj.update(operator(recipe_raw))

    return recipe_obj


class Scraper(ABC):
    def __init__(self):
        self.raw_recipes = []
        self.recipes = []

    @abstractproperty
    def url(self):
        return None

    @abstractmethod
    def get_recipes(self):
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

    def process_recipes(self, *operators):
        list(
            map(
                lambda recipe: _process_recipe(recipe, *operators),
                zip(self.recipes, self.raw_recipes),
            )
        )

    def show_recipes(self):
        print(json.dumps(self.recipes, indent=2))

    def save_recipes(self):
        save_recipes(self.recipes)
