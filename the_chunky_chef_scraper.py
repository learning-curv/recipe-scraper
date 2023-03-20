import json
import requests
from bs4 import BeautifulSoup
from scraper import Scraper, get_text


def _get_recipe_page(recipe):
    title_element = recipe.find("h2", class_="entry-title")
    link = title_element.find("a", class_="entry-title-link")

    recipe_page = requests.get(link["href"])
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    recipe_results = recipe_soup.find("div", class_="wprm-recipe-the-chunky-chef")

    return [{"title": get_text(title_element), "link": link["href"]}, recipe_results]


class TheChunkyChefScraper(Scraper):
    @property
    def url(self):
        return "https://www.thechunkychef.com/recipe-index/"

    def get_recipes(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="genesis-content")
        recipe_blocks = results.find_all("article", class_="post")

        zipped_list = list(map(_get_recipe_page, recipe_blocks))

        self.recipes, self.raw_recipes = zip(*zipped_list)

        return self

    def get_description(self, recipe):
        recipe_description = get_text(recipe.find("div", class_="wprm-recipe-summary"))

        return {"description": recipe_description}

    def get_author(self, recipe):
        recipe_author_container = recipe.find("span", class_="wprm-recipe-author")
        recipe_author = get_text(
            recipe_author_container.find("a", recursive=False)
            if recipe_author_container
            else None
        )

        return {"author": recipe_author}

    def get_servings(self, recipe):
        recipe_servings = get_text(recipe.find("span", class_="wprm-recipe-servings"))

        return {"servings": recipe_servings}

    def get_prep_time(self, recipe):
        recipe_prep_time = get_text(recipe.find("span", class_="wprm-recipe-prep_time"))
        recipe_prep_time_unit = get_text(
            recipe.find("span", class_="wprm-recipe-prep_time-unit")
        )

        return {"prep_time": {"time": recipe_prep_time, "unit": recipe_prep_time_unit}}

    def get_cook_time(self, recipe):
        recipe_cook_time = get_text(recipe.find("span", class_="wprm-recipe-cook_time"))
        recipe_cook_time_unit = get_text(
            recipe.find("span", class_="wprm-recipe-cook_time-unit")
        )

        return {"cook_time": {"time": recipe_cook_time, "unit": recipe_cook_time_unit}}
