import pytest
from unittest.mock import patch
from recipe.models.themealdb_model import RecipeAPI

@pytest.fixture()
def recipe_api():
    """Fixture to provide a new instance of RecipeAPI for each test."""
    return RecipeAPI()

@patch("recipe.models.themealdb_model.requests.get")
def test_search_meals_by_name(mock_get, recipe_api):
    """Test searching meals by name."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"meals": [{"idMeal": "1", "strMeal": "Arrabiata"}]}
    
    result = recipe_api.search_meals_by_name("Arrabiata")
    assert len(result) == 1
    assert result[0]["strMeal"] == "Arrabiata"

@patch("recipe.models.themealdb_model.requests.get")
def test_get_meal_details(mock_get, recipe_api):
    """Test fetching meal details by ID."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"meals": [{"idMeal": "1", "strMeal": "Arrabiata"}]}
    
    result = recipe_api.get_meal_details("1")
    assert result is not None
    assert result["strMeal"] == "Arrabiata"

@patch("recipe.models.themealdb_model.requests.get")
def test_get_random_meal(mock_get, recipe_api):
    """Test fetching a random meal."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"meals": [{"idMeal": "1", "strMeal": "Random Meal"}]}
    
    result = recipe_api.get_random_meal()
    assert result is not None
    assert result["strMeal"] == "Random Meal"

@patch("recipe.models.themealdb_model.requests.get")
def test_list_meals_by_first_letter(mock_get, recipe_api):
    """Test listing meals by first letter."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"meals": [{"idMeal": "1", "strMeal": "Apple Pie"}]}
    
    result = recipe_api.list_meals_by_first_letter("A")
    assert len(result) == 1
    assert result[0]["strMeal"] == "Apple Pie"

@patch("recipe.models.themealdb_model.requests.get")
def test_filter_meals_by_ingredient(mock_get, recipe_api):
    """Test filtering meals by ingredient."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"meals": [{"idMeal": "1", "strMeal": "Chicken Soup"}]}
    
    result = recipe_api.filter_meals_by_ingredient("chicken")
    assert len(result) == 1
    assert result[0]["strMeal"] == "Chicken Soup"

@patch("recipe.models.themealdb_model.requests.get")
def test_handle_api_errors(mock_get, recipe_api):
    """Test handling API errors gracefully."""
    # Set the mock to raise an exception when it is called
    mock_get.side_effect = Exception("API error")
    
    # Test that each method handles the error gracefully
    assert recipe_api.search_meals_by_name("NonExistent") == []
    assert recipe_api.get_meal_details("9999") is None
    assert recipe_api.get_random_meal() is None
    assert recipe_api.list_meals_by_first_letter("Z") == []
    assert recipe_api.filter_meals_by_ingredient("unknown") == []

