"""
Configuration using dataclasses.
Customize these for your project's tunable parameters.
"""

from dataclasses import dataclass


@dataclass
class AppConfig:
    """Main application settings"""

    debug: bool = False
    log_level: str = "INFO"


@dataclass
class DatabaseConfig:
    """Database connection settings (example)"""

    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"


# Global instances - customize these for your project
app_config = AppConfig()
db_config = DatabaseConfig()
