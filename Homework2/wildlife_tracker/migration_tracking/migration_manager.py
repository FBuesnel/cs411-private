from typing import Optional, Any
from migration import Migration

class MigrationManager:
    def __init__(self) -> None:
        migrations: dict[int, Migration] = {}

    def schedule_migration(migration_path: MigrationPath) -> None:
        # Not implemented
        pass

    def update_migration_details(migration_id: int, **kwargs: Any) -> None:
        # Not implemented
        pass

    def cancel_migration(migration_id: int) -> None:
        # Not implemented
        pass

    def get_migrations_by_start_date(start_date: str) -> list[Migration]:
        # Not implemented
        pass

    def get_migrations_by_status(status: str) -> list[Migration]:
        # Not implemented
        pass


    def get_migrations_by_current_location(current_location: str) -> list[Migration]:
        # Not implemented
        pass