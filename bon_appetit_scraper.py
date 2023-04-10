import json
import requests
from bs4 import BeautifulSoup
from scraper import Scraper, get_text


def _get_recipe_page(recipe):
    link = recipe.find("a", class_="summary-item__hed-link")
    description_element = recipe.find("div", class_="summary-item__dek")

    title_element = link.find("h3", "summary-item__hed")

    link_text = "https://www.bonappetit.com" + link["href"]

    recipe_page = requests.get(link_text)
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    recipe_results = recipe_soup.find("main", class_="page__main-content")

    title_text = get_text(title_element)

    print(title_text)

    return [
        {
            "title": title_text,
            "link": link_text,
            "description": get_text(description_element),
        },
        recipe_results,
    ]


class BonAppetitScraper(Scraper):
    @property
    def url(self):
        return "https://www.bonappetit.com/recipes"

    def get_recipes(self):
        page = requests.get(self.url + f"?page={1}")
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="summary-list__items")

        recipe_blocks = [
            item
            for list_set in results
            for item in list_set.find_all("div", class_="summary-item--recipe")
        ]

        pageIndex = 2

        while results:
            print("page: " + self.url + f"?page={pageIndex}")
            page = requests.get(self.url + f"?page={pageIndex}")
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find_all("div", class_="summary-list__items")

            if not results:
                print("break")
                break

            recipe_blocks += [
                item
                for list_set in results
                for item in list_set.find_all("div", class_="summary-item--recipe")
            ]

            pageIndex += 1

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
        servings_container = recipe.find("div", attrs={"data-testid": "IngredientList"})
        servings = servings_container.find("p")

        if not servings:
            return {"servings": None}

        return {"servings": get_text(servings)}

    def get_prep_time(self, recipe):
        return {"prep-time": None}

    def get_cook_time(self, recipe):
        return {"cook-time": None}

    def get_ingredient_groups(self, recipe):
        pass

    def get_instruction_groups(self, recipe):
        pass
