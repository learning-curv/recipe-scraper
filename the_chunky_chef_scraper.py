import requests
from bs4 import BeautifulSoup
from scraper import Scraper, get_text


def _get_recipe_page(recipe):
    title_element = recipe.find("h2", class_="entry-title")
    link = title_element.find("a", class_="entry-title-link")

    recipe_page = requests.get(link["href"])
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    recipe_results = recipe_soup.find("div", class_="wprm-recipe-the-chunky-chef")

    title_text = get_text(title_element)

    print(title_text)

    return [{"title": title_text, "link": link["href"]}, recipe_results]


def find_ingredient_info(ingredient):
    amount = ingredient.find("span", class_="wprm-recipe-ingredient-amount")
    unit = ingredient.find("span", class_="wprm-recipe-ingredient-unit")
    name = ingredient.find("span", class_="wprm-recipe-ingredient-name")
    notes = ingredient.find("span", class_="wprm-recipe-ingredient-notes")

    return {
        "amount": get_text(amount),
        "unit": get_text(unit),
        "name": get_text(name),
        "notes": get_text(notes),
    }


def find_ingredient_group_info(group):
    group_title = group.find("h4", class_="wprm-recipe-group-name")
    group_ingredients_raw = group.find_all("li", "wprm-recipe-ingredient")
    group_ingredients = list(map(find_ingredient_info, group_ingredients_raw))

    return {"title": get_text(group_title), "ingredients": group_ingredients}


def find_instruction_group_info(group):
    title = get_text(group.find("h4", "wprm-recipe-instruction-group-name"))
    instructions = group.find_all("div", "wprm-recipe-instruction-text")
    return {
        "title": title,
        "instructions": list(
            map(lambda instruction: get_text(instruction), instructions)
        ),
    }


class TheChunkyChefScraper(Scraper):
    @property
    def url(self):
        return "https://www.thechunkychef.com/recipe-index/"

    def get_recipes(self):
        print("page: 1")
        page = requests.get(self.url + "page/" + str(132))
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="genesis-content")
        recipe_blocks = results.find_all("article", class_="post")

        next_button = results.find("li", class_="pagination-next")
        pageIndex = 2

        while next_button:
            print("page: " + str(pageIndex))
            page = requests.get(self.url + "page/" + str(pageIndex))
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="genesis-content")
            recipe_blocks += results.find_all("article", class_="post")

            next_button = results.find("li", class_="pagination-next")
            pageIndex += 1

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

    def get_ingredient_groups(self, recipe):
        ingredient_groups_raw = recipe.find_all(
            "div", class_="wprm-recipe-ingredient-group"
        )
        ingredient_groups = list(map(find_ingredient_group_info, ingredient_groups_raw))

        return {"ingredient_groups": ingredient_groups}

    def get_instruction_groups(self, recipe):
        recipe_instruction_groups_raw = recipe.find_all(
            "div", "wprm-recipe-instruction-group"
        )
        recipe_instruction_groups = list(
            map(find_instruction_group_info, recipe_instruction_groups_raw)
        )

        return {"instruction_groups": recipe_instruction_groups}
