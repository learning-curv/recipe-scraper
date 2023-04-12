import json
import requests
from bs4 import BeautifulSoup
from uuid import UUID, uuid5

from scraper import Scraper, get_text
from logging_config import logger

NAMESPACE = UUID("8b4f88c6-a5ea-4dac-8a59-7517c6e00981")


def _get_recipe_page(recipe):
    link = recipe.find("a", class_="summary-item__hed-link")
    description_element = recipe.find("div", class_="summary-item__dek")

    title_element = link.find("h3", "summary-item__hed")

    link_text = "https://www.bonappetit.com" + link["href"]

    recipe_page = requests.get(link_text)
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    recipe_results = recipe_soup.find("main", class_="page__main-content")

    title_text = get_text(title_element)

    logger.info(str(uuid5(NAMESPACE, link_text)) + " " + title_text + " " + link_text)

    return [
        {
            "title": title_text,
            "link": link_text,
            "description": get_text(description_element),
        },
        recipe_results,
    ]


def _map_recipe_ingredients(ingredient):
    amount = get_text(ingredient[0])
    name = get_text(ingredient[1])

    if amount == "¼":
        amount = 0.25
    elif amount == "½":
        amount = 0.5
    elif amount == "¾":
        amount = 0.75

    name = name.replace("\u201d", "-inch")

    return {"amount": amount, "name": name, "unit": None}


class BonAppetitScraper(Scraper):
    @property
    def url(self):
        return "https://www.bonappetit.com/recipes"

    def should_continue(self, page_index):
        page = requests.get(self.url + f"?page={page_index}")
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="summary-list__items")

        if not results:
            logger.info("stop condition reached")

        return bool(results)

    def get_recipes(self, page_index):
        page = requests.get(self.url + f"?page={page_index}")
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="summary-list__items")

        recipe_blocks = [
            item
            for list_set in results
            for item in list_set.find_all("div", class_="summary-item--recipe")
        ]

        zipped_list = list(map(_get_recipe_page, recipe_blocks))

        self.recipes, self.raw_recipes = zip(*zipped_list)

    def get_description(self, recipe):
        return {}

    def get_author(self, recipe):
        recipe_author_element = recipe.find("a", class_="byline__name-link")

        if not recipe_author_element:
            return {"author": "Bon Appetit"}

        return {"author": get_text(recipe_author_element)}

    def get_image_link(self, recipe):
        image_container = recipe.find("img", class_="responsive-image__image")

        if not image_container:
            return {"image-link": None}

        return {"image-link": image_container["src"]}

    def get_servings(self, recipe):
        ingredient_block = recipe.find("div", attrs={"data-testid": "IngredientList"})

        if not ingredient_block:
            return {"servings": None}

        servings = ingredient_block.find("p")

        if not servings:
            return {"servings": None}

        return {"servings": get_text(servings)}

    def get_prep_time(self, recipe):
        return {"prep-time": None}

    def get_cook_time(self, recipe):
        return {"cook-time": None}

    def get_ingredient_groups(self, recipe):
        ingredient_block = recipe.find("div", attrs={"data-testid": "IngredientList"})

        ingredient_list = ingredient_block.find("div")

        ingredient_amount_list = ingredient_list.find_all("p")
        ingredient_name_list = ingredient_list.find_all("div")

        zipped = zip(ingredient_amount_list, ingredient_name_list)

        ingredients = list(map(_map_recipe_ingredients, zipped))

        return {"ingredient_groups": [{"title": None, "ingredients": ingredients}]}

    def get_instruction_groups(self, recipe):
        instruction_block = recipe.find(
            "div", attrs={"data-testid": "InstructionsWrapper"}
        )
        instruction_list = instruction_block.find("li")

        instructions = instruction_list.find_all("p")

        instructions = list(map(lambda i: get_text(i), instructions))

        return {"instruction_groups": [{"title": None, "instructions": instructions}]}
