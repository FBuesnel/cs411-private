import pytest
import sqlite3
from contextlib import contextmanager
from meal_max.models.kitchen_model import (
    Meal,
    create_meal,
    clear_meals,
    delete_meal,
    get_leaderboard,
    get_meal_by_id,
    get_meal_by_name,
    update_meal_stats
)
from unittest.mock import patch
import re

######################################################
#
# Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()


@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    @contextmanager
    def mock_get_db_connection():
        yield mock_conn

    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor

######################################################
#
# Meal Creation and Clear
#
######################################################

def test_create_meal(mock_cursor):
    """Test creating a new meal in the database."""
    create_meal(meal="Pasta", cuisine="Italian", price=15.99, difficulty="MED")

    expected_query = normalize_whitespace("INSERT INTO meals (meal, cuisine, price, difficulty) VALUES (?, ?, ?, ?)")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query

    expected_args = ("Pasta", "Italian", 15.99, "MED")
    actual_args = mock_cursor.execute.call_args[0][1]
    assert actual_args == expected_args, f"Expected arguments {expected_args}, got {actual_args}"

def test_create_meal_negative_price():
    """Test creating a meal with a negative price."""
    with pytest.raises(ValueError, match="Invalid price: -10. Price must be a positive number."):
        create_meal(meal="Pasta", cuisine="Italian", price=-10, difficulty="MED")

def test_create_meal_invalid_difficulty():
    """Test creating a meal with invalid difficulty level."""
    with pytest.raises(ValueError, match="Invalid difficulty level: HARD. Must be 'LOW', 'MED', or 'HIGH'."):
        create_meal(meal="Pasta", cuisine="Italian", price=10, difficulty="HARD")

def test_clear_meals(mock_cursor, mocker):
    """Test clearing all meals from the database."""
    mocker.patch("builtins.open", mocker.mock_open(read_data="DELETE FROM meals;"))

    clear_meals()

    assert mock_cursor.executescript.called, "Expected executescript to be called for clearing meals."



######################################################
#
# Meal Deletion
#
######################################################

def test_delete_meal(mock_cursor):
    """Test deleting a meal that exists."""
    mock_cursor.fetchone.return_value = (False,)  # Mock meal not deleted

    delete_meal(1)
    expected_query = "UPDATE meals SET deleted = TRUE WHERE id = ?"
    assert mock_cursor.execute.call_args[0][0] == expected_query

def test_delete_meal_already_deleted(mock_cursor):
    """Test deleting a meal that is already marked as deleted."""
    mock_cursor.fetchone.return_value = (True,)  # Mock meal already deleted

    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        delete_meal(1)

######################################################
#
# Retrieving Meals by Name/ID
#
######################################################

def test_get_meal_by_id(mock_cursor):
    """Test retrieving a meal by ID."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 10.0, "MED", False)
    
    meal = get_meal_by_id(1)
    assert meal.meal == "Pasta" and meal.cuisine == "Italian"

def test_get_meal_by_id_deleted(mock_cursor):
    """Test retrieving a meal by ID that has been deleted."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 10.0, "MED", True)
    
    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        get_meal_by_id(1)

def test_get_meal_by_name(mock_cursor):
    """Test retrieving a meal by name."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 10.0, "MED", False)
    
    meal = get_meal_by_name("Pasta")
    assert meal.meal == "Pasta" and meal.cuisine == "Italian"

######################################################
#
# Update Meal Stats Win
#
######################################################

def test_update_meal_stats_win(mock_cursor):
    """Test updating meal stats with a win."""
    mock_cursor.fetchone.return_value = (False,)  # Mock meal not deleted

    update_meal_stats(1, "win")
    assert mock_cursor.execute.call_args[0][0] == "UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?"


######################################################
#
# Leaderboard Retrieval
#
######################################################

def test_get_leaderboard_by_wins(mock_cursor):
    """Test getting the leaderboard sorted by wins."""
    mock_cursor.fetchall.return_value = [(1, "Pasta", "Italian", 10.0, "MED", 10, 8, 0.8)]
    
    leaderboard = get_leaderboard("wins")
    assert leaderboard[0]["meal"] == "Pasta" and leaderboard[0]["win_pct"] == 80.0

def test_get_leaderboard_invalid_sort_by():
    """Test retrieving the leaderboard with an invalid sort_by parameter."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter: rating"):
        get_leaderboard("rating")