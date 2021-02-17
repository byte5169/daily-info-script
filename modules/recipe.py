import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_recipe_key")


def get_recipe():
    url_id = f"https://api.spoonacular.com/recipes/complexSearch?type=breakfast&number=1&maxReadyTime=20&sort=random&apiKey={api_key}"

    response = requests.get(url_id)
    response_json = response.json()

    recipe_id = response_json["results"][0]["id"]

    time.sleep(3)

    url_recipe = (
        f"https://api.spoonacular.com/recipes/{recipe_id}/information?&apiKey={api_key}"
    )

    response = requests.get(url_recipe)
    response_json = response.json()

    recipe_link = response_json["spoonacularSourceUrl"]

    return recipe_link
