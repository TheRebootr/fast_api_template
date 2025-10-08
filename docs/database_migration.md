# Database Migrations - Quick Reference

## Quick Commands (Just)

```bash
# Create migration from model changes (recommended)
just create-migration "add user table"

# Apply all pending migrations
just migrate

# Rollback last migration
uv run alembic downgrade -1

# Show current migration version
uv run alembic current

# Show migration history
uv run alembic history
```

## Common Workflows

### 1. Add a New Table

**Step 1:** Create the SQLAlchemy model in `app/models/`

```python
# app/models/product.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

class Product(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
```

**Step 2:** Register in `app/models/__init__.py`

```python
from app.models.product import Product  # Add this

__all__ = ["User", "Conversation", "Product"]  # Add to __all__
```

**Step 3:** Generate and apply migration

```bash
just create-migration "add product table"
# Review generated file in alembic/versions/
just migrate
```

### 2. Add/Modify a Column to Existing Table

**Step 1:** Update the model

```python
# app/models/user.py
class User(Base, TimestampMixin, VersionMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "users"

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=False) # Changed
    # New column
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
```

**Step 2:** Generate and apply migration

```bash
just create-migration "add email to users; modify title to nullable"
just migrate
```

### 3. Add a Foreign Key Relationship

**Step 1:** Update the model

```python
# app/models/order.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Order(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "orders"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="orders")
```

**Step 2:** Update related model

```python
# app/models/user.py
class User(Base, ...):
    # Add relationship
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
```

**Step 3:** Generate and apply

```bash
just create-migration "add order user relationship"
just migrate
```

## Manual Migrations

### When to Use Manual Migrations

- Complex data transformations
- Custom SQL operations
- Splitting/merging tables
- Renaming columns (autogenerate may drop/recreate)

### Create Empty Migration

```bash
uv run alembic revision -m "custom data migration"
```

### Example: Data Migration

```python
# alembic/versions/<timestamp>_migrate_user_data.py
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Custom data transformation
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            UPDATE users
            SET name = CONCAT(first_name, ' ', last_name)
            WHERE name IS NULL
        """)
    )

def downgrade() -> None:
    # Reverse the transformation
    pass  # Cannot reliably reverse this operation
```

### Example: Custom SQL

```python
def upgrade() -> None:
    # Create a view
    op.execute("""
        CREATE VIEW active_users AS
        SELECT * FROM users
        WHERE updated_at >= NOW() - INTERVAL '30 days'
    """)

def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS active_users")
```

## Migration Commands Reference

### Basic Commands

```bash
# Show verbose history with diffs
uv run alembic history --verbose

# Upgrade to specific revision
uv run alembic upgrade <revision>

# Downgrade to specific revision
uv run alembic downgrade <revision>

# Downgrade by N steps
uv run alembic downgrade -2

# Show SQL without executing
uv run alembic upgrade head --sql

# Stamp database without running migrations
uv run alembic stamp head
```

### Advanced Commands

```bash
# Show pending migrations
uv run alembic current
uv run alembic heads

# Merge multiple heads
uv run alembic merge -m "merge branches" <rev1> <rev2>

# Show specific revision
uv run alembic show <revision>

# Generate SQL for upgrade
uv run alembic upgrade head --sql > migration.sql
```

## Rollback Strategies

### Rollback Last Migration

```bash
# Method 1: Using Just
just migrate-down

# Method 2: Using Alembic directly
uv run alembic downgrade -1
```

### Rollback to Specific Version

```bash
# Get revision ID from history
uv run alembic history

# Rollback to that revision
uv run alembic downgrade <revision_id>
```

### Rollback All Migrations

```bash
uv run alembic downgrade base
```

## Troubleshooting

### Migration Was Applied but Has Errors

```bash
# 1. Rollback the migration
just migrate-down

# 2. Fix the migration file
# Edit alembic/versions/<timestamp>_*.py

# 3. Re-apply
just migrate
```

### Delete Unapplied Migration

```bash
# 1. Check current version
uv run alembic current

# 2. Delete the migration file
rm alembic/versions/<timestamp>_*.py

# 3. Verify
uv run alembic history
```

### Migration Out of Sync

```bash
# Stamp database to specific revision (dangerous!)
uv run alembic stamp <revision_id>

# Or reset to current state
uv run alembic stamp head
```

### Merge Conflicts in Migrations

```bash
# If you have multiple heads (branches)
uv run alembic heads

# Merge them
uv run alembic merge -m "merge migration branches" <head1> <head2>

# Apply the merge
just migrate
```

## Best Practices

### ✅ Do

- **Always review** autogenerated migrations before applying
- **Test migrations** on development database first
- **Use descriptive** migration messages
- **Keep migrations small** - one logical change per migration
- **Add comments** in migration scripts for complex operations
- **Backup production** database before running migrations
- **Write reversible** migrations when possible (implement `downgrade()`)
- **Test rollback** procedure in development

### ❌ Don't

- **Never** edit applied migrations (create a new one instead)
- **Never** delete migrations that exist in production
- **Don't** mix data and schema changes in the same migration (separate them)
- **Don't** use `DROP TABLE` without backups
- **Don't** forget to update model relationships
- **Don't** skip migration review ("it's auto-generated, it's fine" ❌)

## Project-Specific Notes

### Models Location

All SQLAlchemy models are in `app/models/`

### Base Classes

- `Base` - SQLAlchemy declarative base
- `TimestampMixin` - Adds `created_at`, `updated_at`
- `VersionMixin` - Adds `version` for optimistic locking
- `UUIDPrimaryKeyMixin` - Adds UUID `id` primary key

### Database Configuration

- Provider: Set via `POSTGRES_PROVIDER` env variable
- Local: PostgreSQL via asyncpg
- Production: Databricks (future)
- Connection: Async SQLAlchemy 2.0

### Migration Files Location

`alembic/versions/` - All migration scripts

### Configuration

`alembic.ini` - Alembic configuration
`alembic/env.py` - Migration environment setup

## Tips

💡 **Use Just commands** - Simpler than remembering Alembic syntax
💡 **Check `git diff`** - Review model changes before creating migration
💡 **Name migrations well** - Use descriptive, action-oriented names
💡 **One change type** - Don't mix adding tables with modifying columns
💡 **Test both ways** - Always test upgrade AND downgrade
💡 **Document data migrations** - Add comments explaining WHY, not just WHAT

## Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- Project models: `app/models/`
- Migration history: `alembic/versions/`
- Just commands: `justfile`
