"""Tests for configuration management."""

import pytest

from app.config import Config, EnvironmentType, PostgresType


def test_config_is_production():
    """Test the is_production property."""
    # Test production environment
    config = Config(ENVIRONMENT=EnvironmentType.PRODUCTION)
    assert config.is_production is True

    # Test non-production environments
    config_dev = Config(ENVIRONMENT=EnvironmentType.DEVELOPMENT)
    assert config_dev.is_production is False

    config_test = Config(ENVIRONMENT=EnvironmentType.TEST)
    assert config_test.is_production is False


def test_config_environment_enum_validation():
    """Test that Config validates environment values against enum."""
    # Valid enum values should work
    config = Config(ENVIRONMENT=EnvironmentType.PRODUCTION)
    assert config.ENVIRONMENT == EnvironmentType.PRODUCTION

    # String values matching enum should work
    config_str = Config(ENVIRONMENT="development")
    assert config_str.ENVIRONMENT == EnvironmentType.DEVELOPMENT

    # Invalid values should raise validation error
    with pytest.raises(Exception):  # Pydantic ValidationError
        Config(ENVIRONMENT="invalid_env")


def test_config_postgres_provider_enum_validation():
    """Test that Config validates postgres provider against enum."""
    # Valid enum values should work
    config = Config(POSTGRES_PROVIDER=PostgresType.LOCAL)
    assert config.POSTGRES_PROVIDER == PostgresType.LOCAL

    config_db = Config(POSTGRES_PROVIDER=PostgresType.DATABRICKS)
    assert config_db.POSTGRES_PROVIDER == PostgresType.DATABRICKS

    # Invalid values should raise validation error
    with pytest.raises(Exception):  # Pydantic ValidationError
        Config(POSTGRES_PROVIDER="invalid_provider")


def test_config_custom_values():
    """Test that Config can be initialized with custom values."""
    config = Config(
        ENVIRONMENT=EnvironmentType.DEVELOPMENT,
        DEBUG=True,
        APP_VERSION="1.0.0",
        ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"],
        POSTGRES_PROVIDER=PostgresType.DATABRICKS,
    )

    assert config.ENVIRONMENT == EnvironmentType.DEVELOPMENT
    assert config.DEBUG is True
    assert config.APP_VERSION == "1.0.0"
    assert len(config.ALLOWED_ORIGINS) == 2
    assert "http://localhost:3000" in config.ALLOWED_ORIGINS
    assert config.POSTGRES_PROVIDER == PostgresType.DATABRICKS


def test_config_from_env_vars(monkeypatch):
    """Test that Config loads from environment variables using monkeypatch."""
    # Use pytest's monkeypatch fixture instead of unittest.mock.patch
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("APP_VERSION", "2.0.0")
    monkeypatch.setenv("POSTGRES_PROVIDER", "databricks")

    config = Config()
    assert config.ENVIRONMENT == EnvironmentType.PRODUCTION
    assert config.DEBUG is False
    assert config.APP_VERSION == "2.0.0"
    assert config.POSTGRES_PROVIDER == PostgresType.DATABRICKS


def test_config_database_settings():
    """Test database configuration settings."""
    config = Config(
        DATABASE_URL="postgresql+asyncpg://test:test@localhost/testdb",
        DATABASE_ECHO=True,
    )

    assert (
        config.DATABASE_URL
        == "postgresql+asyncpg://test:test@localhost/testdb"
    )
    assert config.DATABASE_ECHO is True


@pytest.mark.parametrize(
    "env_type,expected_production,expected_development,expected_test",
    [
        (EnvironmentType.PRODUCTION, True, False, False),
        (EnvironmentType.DEVELOPMENT, False, True, False),
        (EnvironmentType.TEST, False, False, True),
    ],
)
def test_config_environment_properties_parametrized(
    env_type, expected_production, expected_development, expected_test
):
    """Test environment check properties with parametrized inputs."""
    config = Config(ENVIRONMENT=env_type)

    assert config.is_production == expected_production


@pytest.mark.parametrize(
    "provider_type",
    [PostgresType.LOCAL, PostgresType.DATABRICKS],
)
def test_config_postgres_provider_types(provider_type):
    """Test different postgres provider types."""
    config = Config(POSTGRES_PROVIDER=provider_type)
    assert config.POSTGRES_PROVIDER == provider_type
