import logging
from typing import Any, List

from recipe.clients.mongo_client import sessions_collection
from recipe.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


def login_user(user_id: int, RecipeManager) -> None:
    """
    Load the user's recipes from MongoDB into the RecipeManager's shopping list.

    Checks if a session document exists for the given `user_id` in MongoDB.
    If it exists, clears any current recipes in `RecipeManager` and loads
    the stored recipes from MongoDB into `RecipeManager`.

    If no session is found, it creates a new session document for the user
    with an empty recipes list in MongoDB.

    Args:
        user_id (int): The ID of the user whose session is to be loaded.
        RecipeManager (RecipeManager): An instance of `RecipeManager` where the user's shopping list
                                    will be loaded.
    """
    logger.info("Attempting to log in user with ID %d.", user_id)
    session = sessions_collection.find_one({"user_id": user_id})

    if session:
        logger.info("Session found for user ID %d. Loading recipes into RecipeManagerl.", user_id)
        RecipeManager.clear_shopping_list()
        for recipe in session.get("recipes", []):
            logger.debug("Preparing recipe: %s", recipe)
            RecipeManager.add_to_shopping_list(recipe, 1)
        logger.info("recipes successfully loaded for user ID %d.", user_id)
    else:
        logger.info("No session found for user ID %d. Creating a new session with empty recipes list.", user_id)
        sessions_collection.insert_one({"user_id": user_id, "recipes": []})
        logger.info("New session created for user ID %d.", user_id)

def logout_user(user_id: int, RecipeManager) -> None:
    """
    Store the current recipes from the RecipeManager back into MongoDB.

    Retrieves the current recipes from `RecipeManager` and attempts to store them in
    the MongoDB session document associated with the given `user_id`. If no session
    document exists for the user, raises a `ValueError`.

    After saving the recipes to MongoDB, the recipes list in `RecipeManager` is
    cleared to ensure a fresh state for the next login.

    Args:
        user_id (int): The ID of the user whose session data is to be saved.
        RecipeManager (BattleModel): An instance of `BattleModel` from which the user's
                                    current recipes are retrieved.

    Raises:
        ValueError: If no session document is found for the user in MongoDB.
    """
    logger.info("Attempting to log out user with ID %d.", user_id)
    recipes_data = RecipeManager.get_shopping_list()
    logger.debug("Current recipes for user ID %d: %s", user_id, recipes_data)

    result = sessions_collection.update_one(
        {"user_id": user_id},
        {"$set": {"recipes": recipes_data}},
        upsert=False  # Prevents creating a new document if not found
    )

    if result.matched_count == 0:
        logger.error("No session found for user ID %d. Logout failed.", user_id)
        raise ValueError(f"User with ID {user_id} not found for logout.")

    logger.info("recipes successfully saved for user ID %d. Clearing BattleModel recipes.", user_id)
    RecipeManager.clear_shopping_list()
    logger.info("BattleModel recipes cleared for user ID %d.", user_id)
