# Web API Project Template

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)

API endpoint web framework, to have a good starting point.

## Developer Setup

The instructions below are tested on any bash/zsh shell (Linux / MacOS / WSL).

### Prerequisites

- **uv** - Fast Python package installer ([Install UV](https://github.com/astral-sh/uv))
- **just** - Command runner ([Install Just](https://github.com/casey/just))

### Project

1. **Clone the repository:**

   ```bash
   gh repo clone {this repo}
   cd marvis-api
   ```

2. **Run a one-time setup script:**

   ```bash
   just setup
   ```

3. **Start the development server:**

   ```bash
   just dev
   ```

### VS Code

This repository includes VS Code configuration for optimal development experience.

#### Recommended Extensions

- **Python** (`ms-python.python`) - Python language support
- **Pylance** (`ms-python.vscode-pylance`) - Fast Python language server
- **Ruff** (`charliermarsh.ruff`) - Fast Python linter & formatter
- **Python Debugger** (`ms-python.debugpy`) - Debugger
- **DotENV** (`mikestead.dotenv`) - env files support
- **GitHub Pull Requests** (`GitHub.vscode-pull-request-github`) - Pull Request for GitHub
- **Even Better TOML** (`tamasfe.even-better-toml`) - Fully-featured TOML support

#### VS Code Features

The workspace configuration(.vscode/settings.json) activates the following:

- ☑️ **Type hints** & **IntelliSense**
- ☑️ **Auto-formatting**
- ☑️ **Auto-import sorting**
- ☑️ **Integrated testing**
- ☑️ **Debug configurations**
- ☑️ **Inline error highlighting**
- ☑️ **AI prompt fo Commit Message & GitHub PR Requests**

## Project Structure

```
project-api/
├── alembic/                   # Database migrations
├── app/                       # Main application code
│   ├── main.py                # FastAPI application entry point
│   ├── config.py              # Configuration via pydantic-settings
│   ├── api/                   # API layer
│   │   ├── dependencies.py    # Shared dependencies (DI)
│   │   └── v1/                # API version 1
│   │       ├── __init__.py    # Router registration
│   ├── core/                  # Core functionality
│   ├── db/                    # Database layer
│   ├── models/                # SQLAlchemy ORM models
│   └── schemas/               # Pydantic schemas
├── docs/                      # Documentation
├── tests/                     # Test suite
├── .env.example               # Example environment variables
├── alembic.ini                # Alembic configuration
├── justfile                   # Task runner commands
├── pyproject.toml             # Project dependencies & config

```

## Database Migrations

This project uses **Alembic** for database schema migrations with SQLAlchemy 2.0.
For more details, see [docs/database_migrations.md](docs/database_migrations.md).

### Creating Migrations

#### 1. Auto-generate from Model Changes

The recommended way to create migrations is to let Alembic auto-detect changes:

```bash
# 1. Update your model in app/models/
# 2. Generate migration
just create-migration "add conversation model"

# 3. Review the generated migration file in alembic/versions/
# 4. Apply the migration
just migrate
```

#### 2. Manual Migration Creation

For complex changes (data migrations, custom SQL):

```bash
# 1. Create empty migration
uv run alembic revision -m "add custom index"

# 2. Edit the generated file in alembic/versions/
# 3. Add your custom upgrade() and downgrade() logic
# 4. Apply the migration
just migrate
```

## Project Status

### Base Architecture

| Component              | Status  | Notes             |
| ---------------------- | ------- | ----------------- |
| Folder structure       | ✅ Done | Repo organization |
| FastAPI                | ✅ Done | Core framework    |
| Pydantic               | ✅ Done | Validation        |
| SQLAlchemy (async)     | ✅ Done | Database ORM      |
| Alembic (sync)         | ✅ Done | Migrations        |
| Postgres (local)       | ✅ Done | Data persistence  |
| Exception handling     | ✅ Done | Error management  |
| Logging (Loguru)       | ✅ Done | Observability     |
| Pytest                 | ✅ Done | Testing framework |
| DevEx (just, uv, ruff) | ✅ Done | Tooling           |
| User Auth              | 🔜 TODO | Authentication    |
| Role Management        | 🔜 TODO | Authorization     |

### Production Readiness

- 🔜 CI/CD Pipeline
- 🔜 Hosting Provider
- 🔜 Identity Provider
- 🔜 Database Management (Migration, Rollback & Env)
- 🔜 Application Metrics
- 🔜 Log Aggregation

---

<div align="center">

### Built by Rob :)

**[Documentation](docs/)** • **[Issues](https://github.com/)** • **[Contributing](CONTRIBUTING.md)**

</div>
