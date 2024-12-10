import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeAPI:
    """
    A class to interact with TheMealDB API.
    """

    BASE_URL = "https://www.themealdb.com/api/json/v1/1"

    def __init__(self):
        """
        Initialize the RecipeAPI client.
        """
        self.headers = {"Content-Type": "application/json"}

    def search_meals_by_name(self, meal_name):
        """
        Search for meals by their name.
        :param meal_name: Name of the meal (e.g., 'Arrabiata').
        :return: List of meals matching the search query.
        """
        url = f"{self.BASE_URL}/search.php?s={meal_name}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Search results for meal name '{meal_name}' fetched successfully.")
            return data.get("meals", [])
        except requests.RequestException as e:
            logger.error(f"Error fetching meals by name: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during meal search: {e}")
            return []

    def get_meal_details(self, meal_id):
        """
        Fetch detailed information about a meal by its ID.
        :param meal_id: ID of the meal.
        :return: A dictionary with meal details.
        """
        url = f"{self.BASE_URL}/lookup.php?i={meal_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Meal details for ID {meal_id} fetched successfully.")
            return data.get("meals", [])[0] if data.get("meals") else None
        except requests.RequestException as e:
            logger.error(f"Error fetching meal details for ID {meal_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during meal details retrieval: {e}")
            return None

    def get_random_meal(self):
        """
        Fetch a random meal.
        :return: A dictionary with random meal details.
        """
        url = f"{self.BASE_URL}/random.php"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info("Random meal fetched successfully.")
            return data.get("meals", [])[0] if data.get("meals") else None
        except requests.RequestException as e:
            logger.error(f"Error fetching random meal: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during random meal retrieval: {e}")
            return None

    def list_meals_by_first_letter(self, letter):
        """
        List all meals starting with a specific letter.
        :param letter: The first letter of the meal name.
        :return: List of meals matching the first letter.
        """
        url = f"{self.BASE_URL}/search.php?f={letter}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Meals starting with letter '{letter}' fetched successfully.")
            return data.get("meals", [])
        except requests.RequestException as e:
            logger.error(f"Error listing meals by first letter '{letter}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during meal listing by first letter '{letter}': {e}")
            return []

    def filter_meals_by_ingredient(self, ingredient):
        """
        Filter meals by a specific ingredient.
        :param ingredient: Ingredient name (e.g., 'chicken_breast').
        :return: List of meals containing the ingredient.
        """
        url = f"{self.BASE_URL}/filter.php?i={ingredient}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Meals filtered by ingredient '{ingredient}' fetched successfully.")
            return data.get("meals", [])
        except requests.RequestException as e:
            logger.error(f"Error filtering meals by ingredient '{ingredient}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during filtering meals by ingredient '{ingredient}': {e}")
            return []
