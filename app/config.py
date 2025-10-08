"""Configuration management using pydantic-settings."""

from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class PostgresType(str, Enum):
    LOCAL = "local"
    DATABRICKS = "databricks"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application settings
    ENVIRONMENT: EnvironmentType = EnvironmentType.PRODUCTION
    DEBUG: bool = False
    APP_VERSION: str = "0.1.0"

    # API settings
    ALLOWED_ORIGINS: list[str] = []

    # Database settings
    POSTGRES_PROVIDER: PostgresType = PostgresType.LOCAL
    DATABASE_URL: str = (
        "postgresql+asyncpg://user:password@localhost:5432/dbname"
    )
    DATABASE_ECHO: bool = False

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE_ENABLED: bool = False
    LOG_FILE_PATH: str = "app/errors.log"
    LOG_FILE_ROTATION: str = "10 MB"
    LOG_FILE_RETENTION: str = "7 days"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == EnvironmentType.PRODUCTION


config: Settings = Settings()
