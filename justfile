# Justfile for marvis-api

# Default recipe to display available commands
default:
    @just --list

# Install dependencies using uv
install:
    uv sync --group dev

# Run the FastAPI development server
dev:
    uv run fastapi dev app/main.py

# Run tests
test:
    uv run pytest

# Run linting with ruff
lint:
    uv run ruff check app tests

# Format code with ruff
fmt:
    uv run ruff format app tests

# Run ruff check, fix & format
fix:
    uv run ruff check --fix app tests
    uv run ruff format app tests

# Generate alembic migration with autogenerate (requires message)
create-migration message:
    uv run alembic revision --autogenerate -m "{{message}}"

# Apply alembic migrations
migrate:
    uv run alembic upgrade head

# Clean up cache files and directories
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    find . -type d -name ".ruff_cache" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

env:
    cp .env.example .env

# Run all quality checks (lint + test)
check: lint test

# Bootstrap for development
setup: install env
    @echo "---------------------------------------------"
    @echo "--------- 🚀 Setup completed ----------------"
    @echo "--- Note: Change the .env file as needed. ---"
    @echo "---------------------------------------------"

