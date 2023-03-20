from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty


def get_text(html):
    return html.text if html else None


def _process_recipe(recipe, *operators):
    recipe_obj, recipe_raw = recipe

    for operator in operators:
        recipe_obj.update(operator(recipe_raw))

    print(recipe_obj)
    return recipe_obj


class Scraper(ABC):
    def __init__(self):
        self.raw_recipes = []
        self.recipes = []

    @abstractproperty
    def url(self):
        return None

    def process_recipes(self, *operators):
        list(
            map(
                lambda recipe: _process_recipe(recipe, *operators),
                zip(self.recipes, self.raw_recipes),
            )
        )

    @abstractmethod
    def get_recipes(self):
        pass

    @abstractmethod
    def process_recipes(self, *operators):
        pass

    @abstractmethod
    def get_descriptions(self, recipe):
        pass

    @abstractmethod
    def get_authors(self):
        pass
