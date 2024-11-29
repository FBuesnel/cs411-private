from typing import Optional
from Homework2.wildlife_tracker.habitat_management.habitat import Habitat
from migration_path import MigrationPath, Migration

class Migration:

    def __init__(self,
                current_date: str,
                current_location: str,
                destination: Habitat,
                migration_id: int,
                migration_path: MigrationPath,
                path_id: int,
                start_date: str,
                start_location: Habitat,
                status: str = "Scheduled",
                duration: Optional[int] = None,
                health_status: Optional[str] = None
                ) -> None:
        self.current_date = current_date
        self.current_location = current_location
        self.destination = destination
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.path_id = path_id
        self.start_date = start_date
        self.start_location = start_location
        self.status = status
        self.duration = duration
        self.health_status = health_status

    def get_migration_paths() -> list[MigrationPath]:
        # Not implemented
        pass
    
    def get_migrations() -> list[Migration]:
        # Not implemented
        pass