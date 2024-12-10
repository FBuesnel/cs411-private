import pytest
from unittest.mock import patch
from recipe.models.recipe_model import Meal
from recipe.models.themealdb_model import RecipeAPI

@pytest.fixture()
def recipe_api():
    """Fixture to provide a new instance of RecipeAPI for each test."""
    return RecipeAPI()

@pytest.fixture
def sample_meal1():
    """Fixture to provide a sample meal."""
    return Meal(1, "Spaghetti Bolognese", ["Pasta", "Tomato", "Beef"], "Italian")

@pytest.fixture
def sample_meal2():
    """Fixture to provide another sample meal."""
    return Meal(2, "Chicken Curry", ["Chicken", "Curry Paste", "Rice"], "Indian")

@pytest.fixture
def sample_meal_list(sample_meal1, sample_meal2):
    """Fixture to provide a sample list of meals."""
    return [sample_meal1, sample_meal2]


##################################################
# Meal Management Test Cases
##################################################

def test_add_meal_to_database(recipe_api, sample_meal1):
    """Test adding a meal to the local database."""
    recipe_api.add_meal(sample_meal1.id, sample_meal1.meal_name, sample_meal1.ingredients, sample_meal1.category)
    assert len(recipe_api.meals) == 1
    assert recipe_api.meals[0].meal_name == "Spaghetti Bolognese"

def test_add_duplicate_meal_to_database(recipe_api, sample_meal1):
    """Test error when adding a duplicate meal to the local database."""
    recipe_api.add_meal(sample_meal1.id, sample_meal1.meal_name, sample_meal1.ingredients, sample_meal1.category)
    with pytest.raises(ValueError, match="Meal with this ID already exists."):
        recipe_api.add_meal(sample_meal1.id, sample_meal1.meal_name, sample_meal1.ingredients, sample_meal1.category)


##################################################
# Shopping List Test Cases
##################################################

def test_add_to_shopping_list(recipe_api):
    """Test adding ingredients to the shopping list."""
    recipe_api.add_to_shopping_list("Tomato", 3)
    assert recipe_api.shopping_list["Tomato"] == 3

def test_update_shopping_list(recipe_api):
    """Test updating the quantity of an ingredient in the shopping list."""
    recipe_api.add_to_shopping_list("Tomato", 3)
    recipe_api.add_to_shopping_list("Tomato", 2)
    assert recipe_api.shopping_list["Tomato"] == 5

def test_get_shopping_list(recipe_api):
    """Test retrieving the shopping list."""
    recipe_api.add_to_shopping_list("Tomato", 3)
    shopping_list = recipe_api.get_shopping_list()
    assert shopping_list == {"Tomato": 3}


##################################################
# API Integration Test Cases
##################################################

@patch("recipe_model.requests.get")
def test_search_meal_by_name(mock_get, recipe_api):
    """Test searching for meals by name."""
    mock_response = {
        "meals": [
            {
                "idMeal": "1",
                "strMeal": "Spaghetti Bolognese",
                "strCategory": "Italian",
                "strIngredient1": "Pasta",
                "strIngredient2": "Tomato",
                "strIngredient3": "Beef",
                "strIngredient4": None,
            }
        ]
    }
    mock_get.return_value.json.return_value = mock_response

    meals = recipe_api.search_meal_by_name("Spaghetti")
    assert len(meals) == 1
    assert meals[0].meal_name == "Spaghetti Bolognese"
    assert meals[0].category == "Italian"
    assert "Tomato" in meals[0].ingredients

@patch("recipe_model.requests.get")
def test_filter_meals_by_ingredient(mock_get, recipe_api):
    """Test filtering meals by ingredient."""
    mock_response = {
        "meals": [
            {
                "idMeal": "1",
                "strMeal": "Spaghetti Bolognese",
                "strIngredient1": "Pasta",
                "strIngredient2": "Tomato",
                "strIngredient3": "Beef",
            }
        ]
    }
    mock_get.return_value.json.return_value = mock_response

    meals = recipe_api.filter_meals_by_ingredient("Tomato")
    assert len(meals) == 1
    assert meals[0].meal_name == "Spaghetti Bolognese"
    assert "Tomato" in meals[0].ingredients

@patch("recipe_model.requests.get")
def test_filter_meals_by_category(mock_get, recipe_api):
    """Test filtering meals by category."""
    mock_response = {
        "meals": [
            {
                "idMeal": "1",
                "strMeal": "Spaghetti Bolognese",
                "strCategory": "Italian",
                "strIngredient1": "Pasta",
                "strIngredient2": "Tomato",
                "strIngredient3": "Beef",
            }
        ]
    }
    mock_get.return_value.json.return_value = mock_response

    meals = recipe_api.filter_meals_by_category("Italian")
    assert len(meals) == 1
    assert meals[0].meal_name == "Spaghetti Bolognese"
    assert meals[0].category == "Italian"
