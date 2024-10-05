from typing import Optional, List
from Homework2.wildlife_tracker.animal_management.animal import Animal
from habitat import Habitat

class HabitatManager:
    def __init__(self) -> None:
        habitats: dict[int, Habitat] = {}

    def assign_animals_to_habitat(self, animals: List[Animal]) -> None:
        # Not implemented
        pass

    def create_habitat(habitat_id: int, geographic_area: str, size: int, environment_type: str) -> Habitat:
        # Not implemented
        pass
    
    def get_animals_in_habitat(habitat_id: int) -> List[Animal]:
        # Not implemented
        pass

    def get_habitat_by_id(habitat_id: int) -> Habitat:
        # Not implemented
        pass

    def get_habitat_details(habitat_id: int) -> dict:
        # Not implemented
        pass

    def get_habitats_by_geographic_area(geographic_area: str) -> List[Habitat]:
        # Not implemented
        pass

    def get_habitats_by_size(size: int) -> List[Habitat]:
        # Not implemented
        pass

    def get_habitats_by_type(environment_type: str) -> List[Habitat]:
        # Not implemented
        pass

    def remove_habitat(habitat_id: int) -> None:
        # Not implemented
        pass