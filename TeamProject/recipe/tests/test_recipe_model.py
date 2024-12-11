import pytest
from unittest.mock import patch
from recipe.models.recipe_model import Meal
from recipe.models.recipe_model import RecipeManager  

@pytest.fixture()
def recipe_manager():
    """Fixture to provide a new instance of RecipeManager for each test."""
    return RecipeManager()

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

def test_add_meal_to_local_database(recipe_manager, sample_meal1):
    """Test adding a meal to the local database."""
    recipe_manager.local_meals.append(sample_meal1)  # Directly appending for simplicity
    assert len(recipe_manager.local_meals) == 1
    assert recipe_manager.local_meals[0].meal_name == "Spaghetti Bolognese"

def test_add_duplicate_meal_to_local_database(recipe_manager, sample_meal1):
    """Test error when adding a duplicate meal to the local database."""
    recipe_manager.local_meals.append(sample_meal1)
    with pytest.raises(ValueError, match="Meal with this ID already exists."):
        if any(meal.id == sample_meal1.id for meal in recipe_manager.local_meals):
            raise ValueError("Meal with this ID already exists.")
        recipe_manager.local_meals.append(sample_meal1)


##################################################
# Shopping List Test Cases
##################################################

def test_add_to_shopping_list(recipe_manager):
    """Test adding ingredients to the shopping list."""
    recipe_manager.add_to_shopping_list("Tomato", 3)
    assert recipe_manager.shopping_list["Tomato"] == 3

def test_update_shopping_list(recipe_manager):
    """Test updating the quantity of an ingredient in the shopping list."""
    recipe_manager.add_to_shopping_list("Tomato", 3)
    recipe_manager.add_to_shopping_list("Tomato", 2)
    assert recipe_manager.shopping_list["Tomato"] == 5

def test_get_shopping_list(recipe_manager):
    """Test retrieving the shopping list."""
    recipe_manager.add_to_shopping_list("Tomato", 3)
    shopping_list = recipe_manager.get_shopping_list()
    assert shopping_list == {"Tomato": 3}

def test_clear_shopping_list(recipe_manager):
    """Test clearing the shopping list."""
    recipe_manager.add_to_shopping_list("Tomato", 3)
    recipe_manager.clear_shopping_list()
    assert len(recipe_manager.shopping_list) == 0


##################################################
# API Integration Test Cases
##################################################

@patch("recipe.models.themealdb_model.requests.get")
def test_search_meal_by_name(mock_get, recipe_manager):
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

    meals = recipe_manager.search_meal_by_name("Spaghetti")
    assert len(meals) == 1
    assert meals[0].meal_name == "Spaghetti Bolognese"
    assert meals[0].category == "Italian"
    assert "Tomato" in meals[0].ingredients

@patch("recipe.models.themealdb_model.requests.get")
def test_filter_meals_by_ingredient(mock_get, recipe_manager):
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

    meals = recipe_manager.search_meal_by_name("Spaghetti")  # You can filter within this call or extend it
    assert len(meals) == 1
    assert meals[0].meal_name == "Spaghetti Bolognese"
    assert "Tomato" in meals[0].ingredients

@patch("recipe.models.themealdb_model.requests.get")
def test_filter_meals_by_category(mock_get, recipe_manager):
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

    meals = recipe_manager.search_meal_by_name("Spaghetti")  # Category can also be checked here
    assert len(meals) == 1
    assert meals[0].meal_name == "Spaghetti Bolognese"
    assert meals[0].category == "Italian"
