import json
import requests
from bs4 import BeautifulSoup
from scraper import Scraper, get_text


def _get_recipe_page(recipe):
    link = recipe.find("a", class_="summary-item__hed-link")
    title_element = link.find("h3", "summary-item__hed")

    link_text = "https://www.bonappetit.com" + link["href"]

    recipe_page = requests.get(link_text)
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    recipe_results = recipe_soup.find("div", class_="wprm-recipe-the-chunky-chef")

    return [{"title": get_text(title_element), "link": link_text}, recipe_results]


class BonAppetitScraper(Scraper):
    @property
    def url(self):
        return "https://www.bonappetit.com/recipes"

    def get_recipes(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="summary-list__items")

        recipe_blocks = [
            item
            for list_set in results
            for item in list_set.find_all("div", class_="summary-item--recipe")
        ]

        zipped_list = list(map(_get_recipe_page, recipe_blocks))
        print(self.recipes)

        self.recipes, self.raw_recipes = zip(*zipped_list)

    def get_description(self, recipe):
        pass

    def get_author(self, recipe):
        pass

    def get_servings(self, recipe):
        pass

    def get_prep_time(self, recipe):
        pass

    def get_cook_time(self, recipe):
        pass

    def get_ingredient_groups(self, recipe):
        pass

    def get_instruction_groups(self, recipe):
        pass
