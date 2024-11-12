import logging
from typing import List

from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.utils.logger import configure_logger
from meal_max.utils.random_utils import get_random

logger = logging.getLogger(__name__)
configure_logger(logger)


class BattleModel:
    """
    A class to manage battles between meal combatants.

    Attributes:
        combatants (List[Meal]): The list of meals set to compete in a battle.
    """

    def __init__(self):
        """
        Initializes the BattleModel with an empty list of combatants.
        """
        self.combatants: List[Meal] = []

    ##################################################
    # Management Functions
    ##################################################

    def prep_combatant(self, combatant_data: Meal) -> None:
        """
        Adds a combatant to the list of combatants if space is available.

        Args:
            combatant_data (Meal): The combatant to add to the list.

        Raises:
            ValueError: If the list of combatants is already full (two combatants).
        """
        if len(self.combatants) >= 2:
            logger.error(
                "Attempted to add combatant '%s' but combatants list is full",
                combatant_data.meal,
            )
            raise ValueError("Combatant list is full, cannot add more combatants.")

        logger.info("Adding combatant '%s' to combatants list", combatant_data.meal)
        self.combatants.append(combatant_data)
        logger.info(
            "Current combatants list: %s",
            [combatant.meal for combatant in self.combatants],
        )

    def clear_combatants(self) -> None:
        """
        Clears the list of combatants.
        """
        logger.info("Clearing the combatants list.")
        self.combatants.clear()

    ##################################################
    # Battle Functions
    ##################################################

    def battle(self) -> str:
        """
        Conducts a battle between two prepped combatants, determining a winner and loser.

        Raises:
            ValueError: If fewer than two combatants are available to start a battle.

        Returns:
            str: The name of the winning meal.
        """
        logger.info("Two meals enter, one meal leaves!")

        if len(self.combatants) < 2:
            logger.error("Not enough combatants to start a battle.")
            raise ValueError("Two combatants must be prepped for a battle.")

        combatant_1 = self.combatants[0]
        combatant_2 = self.combatants[1]

        # Log the start of the battle
        logger.info(
            "Battle started between %s and %s", combatant_1.meal, combatant_2.meal
        )

        # Get battle scores for both combatants
        score_1 = self.get_battle_score(combatant_1)
        score_2 = self.get_battle_score(combatant_2)

        # Log the scores for both combatants
        logger.info("Score for %s: %.3f", combatant_1.meal, score_1)
        logger.info("Score for %s: %.3f", combatant_2.meal, score_2)

        # Compute the delta and normalize between 0 and 1
        delta = abs(score_1 - score_2) / 100
        logger.info("Delta between scores: %.3f", delta)

        # Get random number from random.org
        random_number = get_random()
        logger.info("Random number from random.org: %.3f", random_number)

        # Determine the winner based on the normalized delta
        if delta > random_number:
            winner = combatant_1
            loser = combatant_2
        else:
            winner = combatant_2
            loser = combatant_1

        logger.info("The winner is: %s", winner.meal)

        # Update stats for both combatants
        update_meal_stats(winner.id, "win")
        update_meal_stats(loser.id, "loss")

        # Remove the losing combatant from combatants
        self.combatants.remove(loser)

        return winner.meal

    ##################################################
    # Retrieval Functions
    ##################################################

    def get_combatants(self) -> List[Meal]:
        """
        Retrieves the current list of combatants.

        Returns:
            List[Meal]: A list of combatants in the current battle setup.
        """
        logger.info("Retrieving current list of combatants.")
        return self.combatants

    def get_battle_score(self, combatant: Meal) -> float:
        """
        Calculates a battle score for a combatant based on its price, cuisine, and difficulty.

        Args:
            combatant (Meal): The combatant whose score is to be calculated.

        Returns:
            float: The calculated score for the combatant.
        """
        difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}

        logger.info(
            "Calculating battle score for %s: price=%.3f, cuisine=%s, difficulty=%s",
            combatant.meal,
            combatant.price,
            combatant.cuisine,
            combatant.difficulty,
        )

        score = (combatant.price * len(combatant.cuisine)) - difficulty_modifier[
            combatant.difficulty
        ]
        logger.info("Battle score for %s: %.3f", combatant.meal, score)

        return score