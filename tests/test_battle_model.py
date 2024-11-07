import pytest
from unittest.mock import patch, MagicMock

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal

@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

@pytest.fixture
def sample_meal1():
    return Meal(id=1, meal="Meal 1", price=10.0, cuisine="Italian", difficulty="MED")

@pytest.fixture
def sample_meal2():
    return Meal(id=2, meal="Meal 2", price=15.0, cuisine="Mexican", difficulty="HIGH")

@pytest.fixture
def sample_meal3():
    return Meal(id=3, meal="Meal 3", price=12.0, cuisine="Chinese", difficulty="LOW")

##################################################
# Management Function Test Cases
##################################################

def test_prep_combatant(battle_model, sample_meal1):
    """Test adding a combatant to the battle model."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1, "Expected 1 combatant after adding one"

def test_prep_combatant_full(battle_model, sample_meal1, sample_meal2, sample_meal3):
    """Test adding more than two combatants raises an error."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    with pytest.raises(
        ValueError, match="Combatant list is full, cannot add more combatants."
    ):
        battle_model.prep_combatant(sample_meal3)

def test_clear_combatants(battle_model, sample_meal1, sample_meal2):
    """Test clearing the list of combatants."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    battle_model.clear_combatants()
    assert len(battle_model.combatants) == 0, "Expected no combatants after clearing"

##################################################
# Battle Function Test Cases
##################################################

@patch("meal_max.utils.random_utils.get_random", return_value=0.5)
@patch("meal_max.models.battle_model.update_meal_stats", return_value=None)  # Ensure update_meal_stats is fully mocked
@patch("meal_max.utils.sql_utils.get_db_connection", return_value=MagicMock())  # Mock the database connection
def test_battle(
    mock_get_db_connection, mock_update_meal_stats, mock_get_random, battle_model, sample_meal1, sample_meal2, mocker
):
    """Test a battle between two combatants and verify the winner and stats update."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    winner = battle_model.battle()

    # Ensure one combatant is removed
    assert (
        len(battle_model.combatants) == 1
    ), "Expected only one combatant after the battle"

    # Check that the remaining combatant is the winner
    assert (
        winner == battle_model.combatants[0].meal
    ), "Expected the remaining combatant to be the winner"

    # Check that update_meal_stats was called for both winner and loser
    mock_update_meal_stats.assert_any_call(sample_meal1.id, "win")
    mock_update_meal_stats.assert_any_call(sample_meal2.id, "loss")

def test_battle_insufficient_combatants(battle_model, sample_meal1):
    """Test starting a battle with fewer than two combatants raises an error."""
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(
        ValueError, match="Two combatants must be prepped for a battle."
    ):
        battle_model.battle()

##################################################
# Retrieval Function Test Cases
##################################################

def test_get_combatants(battle_model, sample_meal1, sample_meal2):
    """Test retrieving the list of current combatants."""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    combatants = battle_model.get_combatants()
    assert len(combatants) == 2, "Expected 2 combatants in the list"
    assert combatants[0].meal == "Meal 1", "Expected first combatant to be 'Meal 1'"
    assert combatants[1].meal == "Meal 2", "Expected second combatant to be 'Meal 2'"

##################################################
# Utility Function Test Cases
##################################################

def test_get_battle_score(battle_model, sample_meal1):
    """Test calculating a battle score for a combatant."""
    score = battle_model.get_battle_score(sample_meal1)
    expected_score = (
        sample_meal1.price * len(sample_meal1.cuisine)
    ) - 2  # 'MED' difficulty modifier is 2
    assert (
        score == expected_score
    ), f"Expected score to be {expected_score} but got {score}"
