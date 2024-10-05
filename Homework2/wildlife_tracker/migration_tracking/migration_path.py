from typing import Optional
from migration import Migration
from Homework2.wildlife_tracker.habitat_management.habitat import Habitat

class MigrationPath:
    def __init__(self) -> None:
        paths: dict[int, MigrationPath] = {},

    def get_migration_path_by_id(path_id: int) -> MigrationPath:
        # Not implemented
        pass

    def create_migration_path(species: str, start_location: Habitat, destination: Habitat, duration: Optional[int] = None) -> None:
        # Not implemented
        pass

    def get_migration_paths_by_destination(destination: Habitat) -> list[MigrationPath]:
        # Not implemented
        pass

    def get_migration_paths_by_species(species: str) -> list[MigrationPath]:
        # Not implemented
        pass
    
    def get_migration_paths_by_start_location(start_location: Habitat) -> list[MigrationPath]:
        # Not implemented
        pass

    def get_migrations_by_migration_path(migration_path_id: int) -> list[Migration]:
        # Not implemented
        pass

    def get_migration_path_details(path_id) -> dict:
        # Not implemented
        pass

    def remove_migration_path(path_id: int) -> None:
        # Not implemented
        pass

    def update_migration_path_details(path_id: int, **kwargs) -> None:
        # Not implemented
        pass