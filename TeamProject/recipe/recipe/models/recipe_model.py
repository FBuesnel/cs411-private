import logging
from typing import List, Dict, Optional
from themealdb_model import RecipeAPI  # Import the RecipeAPI

from recipe.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


class Meal:
    """
    Represents a meal with details like name, ingredients, category, and ID.
    """
    def __init__(self, meal_id: int, meal: str, ingredients: List[str], category: str):
        self.id = meal_id
        self.meal_name = meal
        self.ingredients = ingredients
        self.category = category

    def __repr__(self):
        return f"Meal(id={self.id}, meal_name='{self.meal_name}', category='{self.category}')"


class RecipeManager:
    """
    Manages local recipes and interactions with the RecipeAPI.
    """

    def __init__(self):
        self.api = RecipeAPI()  # Initialize the RecipeAPI
        self.local_meals: List[Meal] = []  # Local database of meals
        self.shopping_list: Dict[str, int] = {}  # Shopping list items and quantities

    def search_meal_by_name(self, name: str) -> List[Meal]:
        """
        Searches for meals by name using the external API.

        Args:
            name (str): The name of the meal to search for.

        Returns:
            List[Meal]: A list of Meal objects matching the search criteria.
        """
        logger.info("Searching for meals with name '%s' using RecipeAPI.", name)
        api_results = self.api.search_meals_by_name(name)
        meals = [
            Meal(
                meal_id=int(meal["idMeal"]),
                meal=meal["strMeal"],
                ingredients=self.extract_ingredients(meal),
                category=meal.get("strCategory", "Unknown")
            )
            for meal in api_results
        ]
        return meals

    def get_random_meal(self) -> Optional[Meal]:
        """
        Fetches a random meal from the external API.

        Returns:
            Meal: A random meal object.
        """
        logger.info("Fetching a random meal using RecipeAPI.")
        api_result = self.api.get_random_meal()
        if api_result:
            return Meal(
                meal_id=int(api_result["idMeal"]),
                meal=api_result["strMeal"],
                ingredients=self.extract_ingredients(api_result),
                category=api_result.get("strCategory", "Unknown")
            )
        else:
            logger.warning("No random meal found.")
            return Meal(
                meal_id=0,
                meal="Unknown",
                ingredients=[],
                category="Unknown"
            )

    def add_to_shopping_list(self, ingredient: str, quantity: int):
        """
        Adds an ingredient with its quantity to the shopping list.

        Args:
            ingredient (str): The ingredient to add.
            quantity (int): The quantity of the ingredient.
        """
        if ingredient in self.shopping_list:
            self.shopping_list[ingredient] += quantity
            logger.info("Updated shopping list: %s = %d.", ingredient, self.shopping_list[ingredient])
        else:
            self.shopping_list[ingredient] = quantity
            logger.info("Added to shopping list: %s = %d.", ingredient, quantity)

    def get_shopping_list(self) -> Dict[str, int]:
        """
        Retrieves the current shopping list.

        Returns:
            Dict[str, int]: A dictionary of ingredients and their quantities.
        """
        logger.info("Retrieved shopping list with %d items.", len(self.shopping_list))
        return self.shopping_list

    @staticmethod
    def extract_ingredients(meal_data: dict) -> List[str]:
        """
        Extracts ingredients from the meal data.

        Args:
            meal_data (dict): The meal data from which to extract ingredients.

        Returns:
            List[str]: A list of ingredients.
        """
        ingredients = []
        for i in range(1, 21):  # TheMealDB API includes up to 20 ingredients
            ingredient = meal_data.get(f"strIngredient{i}")
            if ingredient and ingredient.strip():
                ingredients.append(ingredient.strip())
        return ingredients
