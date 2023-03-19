import requests
from bs4 import BeautifulSoup
import json


def get_text(html):
    return html.text if html else None


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


URL = "https://www.thechunkychef.com/recipe-index/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="genesis-content")

recipes = results.find_all("article", class_="post")

for recipe in recipes:
    title_element = recipe.find("h2", class_="entry-title")
    link = title_element.find("a", class_="entry-title-link")

    recipe_page = requests.get(link["href"])
    recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")
    recipe_results = recipe_soup.find("div", class_="wprm-recipe-the-chunky-chef")

    recipe_description = get_text(
        recipe_results.find("div", class_="wprm-recipe-summary")
    )
    recipe_author_container = recipe_results.find("span", class_="wprm-recipe-author")
    recipe_author = get_text(
        recipe_author_container.find("a", recursive=False)
        if recipe_author_container
        else None
    )

    recipe_prep_time = get_text(
        recipe_results.find("span", class_="wprm-recipe-prep_time")
    )
    recipe_prep_time_unit = get_text(
        recipe_results.find("span", class_="wprm-recipe-prep_time-unit")
    )

    recipe_cook_time = get_text(
        recipe_results.find("span", class_="wprm-recipe-cook_time")
    )
    recipe_cook_time_unit = get_text(
        recipe_results.find("span", class_="wprm-recipe-cook_time-unit")
    )

    recipe_servings = get_text(
        recipe_results.find("span", class_="wprm-recipe-servings")
    )

    ingredient_groups_raw = recipe_results.find_all(
        "div", class_="wprm-recipe-ingredient-group"
    )
    ingredient_groups = list(map(find_ingredient_group_info, ingredient_groups_raw))

    recipe_instruction_groups_raw = recipe_results.find_all(
        "div", "wprm-recipe-instruction-group"
    )
    recipe_instruction_groups = list(
        map(find_instruction_group_info, recipe_instruction_groups_raw)
    )

    recipe_json = json.dumps(
        {
            "title": title_element.text,
            "description": recipe_description,
            "author": recipe_author,
            "prep_time": {"time": recipe_prep_time, "unit": recipe_prep_time_unit},
            "cook_time": {"time": recipe_cook_time, "unit": recipe_cook_time_unit},
            "servings": recipe_servings,
            "link": link["href"],
            "ingredient_groups": ingredient_groups,
            "instruction_groups": recipe_instruction_groups,
        },
        indent=2,
    )

    print(recipe_json)
    print()
    print()
    print()
