# Database Migrations Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing database migrations in FastAPI applications using Alembic, covering migration creation, version control, autogenerate patterns, data migrations, rollback strategies, multi-database support, testing migrations, CI/CD integration, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Alembic Setup & Configuration](#alembic-setup--configuration)
3. [Migration Creation](#migration-creation)
4. [Autogenerate Patterns](#autogenerate-patterns)
5. [Data Migrations](#data-migrations)
6. [Version Control](#version-control)
7. [Rollback Strategies](#rollback-strategies)
8. [Multi-Database Support](#multi-database-support)
9. [Testing Migrations](#testing-migrations)
10. [CI/CD Integration](#cicd-integration)
11. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Migration Philosophy

**REQUIRED**: Understand migration principles:

1. **Version Control**: All migrations tracked in version control
2. **Idempotent Operations**: Migrations can be run multiple times safely
3. **Reversible**: Every upgrade has a corresponding downgrade
4. **Atomic**: Migrations execute in transactions
5. **Tested**: Migrations tested before production
6. **Documented**: Clear migration messages and documentation

### When to Use Migrations

**REQUIRED**: Use migrations for:

- **Schema Changes**: Adding/removing tables, columns, indexes
- **Data Transformations**: Migrating data between schema versions
- **Constraint Changes**: Adding/removing constraints, foreign keys
- **Index Management**: Creating/dropping indexes
- **Multi-Environment**: Consistent schema across environments

---

## Alembic Setup & Configuration

### Basic Alembic Configuration

**REQUIRED**: Alembic setup:

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.config import get_settings
from app.db.db_init import Base

# Import all models to ensure they're registered
from app.models.user import UserTable  # noqa: F401
from app.models.gateway_config import EndpointConfig  # noqa: F401

config = context.config

# Override database URL from settings
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

# Set target metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """Execute migrations with connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Run migrations in async mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in online mode."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Alembic Configuration File

**REQUIRED**: `alembic.ini` configuration:

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

---

## Migration Creation

### Autogenerate Migrations

**REQUIRED**: Create migrations with autogenerate:

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add user profiles table"

# Review generated migration before committing
# Edit alembic/versions/xxx_add_user_profiles_table.py
```

### Manual Migrations

**REQUIRED**: Manual migration creation:

```bash
# Create empty migration template
alembic revision -m "Custom data migration"

# Edit the generated file
# alembic/versions/xxx_custom_data_migration.py
```

### Migration File Structure

**REQUIRED**: Migration file template:

```python
"""Add user profiles table

Revision ID: 001_add_user_profiles
Revises: 000_initial_schema
Create Date: 2025-01-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_add_user_profiles'
down_revision = '000_initial_schema'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Apply migration."""
    # Create table
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Create index
    op.create_index('idx_user_profiles_user_id', 'user_profiles', ['user_id'])
    
    # Add column to existing table
    op.add_column('users', sa.Column('profile_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_users_profile', 'users', 'user_profiles', ['profile_id'], ['id'])

def downgrade() -> None:
    """Revert migration."""
    # Remove foreign key
    op.drop_constraint('fk_users_profile', 'users', type_='foreignkey')
    op.drop_column('users', 'profile_id')
    
    # Drop index
    op.drop_index('idx_user_profiles_user_id', 'user_profiles')
    
    # Drop table
    op.drop_table('user_profiles')
```

---

## Autogenerate Patterns

### Autogenerate Best Practices

**REQUIRED**: Autogenerate patterns:

```python
# ✅ Good: Review autogenerated migrations
# 1. Run autogenerate
alembic revision --autogenerate -m "Add email column"

# 2. Review generated migration
# 3. Edit if needed (add data migrations, adjust constraints)
# 4. Test migration
# 5. Commit

# ✅ Good: Handle autogenerate limitations
def upgrade() -> None:
    """Add email column with default."""
    # Autogenerate might not handle defaults correctly
    op.add_column('users', sa.Column('email', sa.String(255), nullable=False))
    
    # Add default value for existing rows
    op.execute("UPDATE users SET email = CONCAT(username, '@example.com') WHERE email IS NULL")
    
    # Add unique constraint
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

# ❌ Bad: Blindly accepting autogenerate
# Always review and test autogenerated migrations
```

### Autogenerate Configuration

**RECOMMENDED**: Configure autogenerate:

```python
# alembic/env.py
def run_migrations_online() -> None:
    """Run migrations with autogenerate configuration."""
    connectable = async_engine_from_config(...)
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Compare column types
            compare_server_default=True,  # Compare defaults
            render_as_batch=True,  # Use batch mode for SQLite
        )
        with context.begin_transaction():
            context.run_migrations()
```

---

## Data Migrations

### Data Migration Patterns

**REQUIRED**: Data migration implementation:

```python
"""Migrate user data to profiles

Revision ID: 002_migrate_user_data
Revises: 001_add_user_profiles
Create Date: 2025-01-14 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002_migrate_user_data'
down_revision = '001_add_user_profiles'

def upgrade() -> None:
    """Migrate user data to profiles."""
    connection = op.get_bind()
    
    # Migrate existing users to profiles
    connection.execute(sa.text("""
        INSERT INTO user_profiles (user_id, bio, created_at, updated_at)
        SELECT id, NULL, created_at, updated_at
        FROM users
        WHERE NOT EXISTS (
            SELECT 1 FROM user_profiles WHERE user_profiles.user_id = users.id
        )
    """))
    
    # Update users with profile_id
    connection.execute(sa.text("""
        UPDATE users
        SET profile_id = (
            SELECT id FROM user_profiles WHERE user_profiles.user_id = users.id
        )
    """))

def downgrade() -> None:
    """Revert data migration."""
    connection = op.get_bind()
    
    # Clear profile_id references
    connection.execute(sa.text("UPDATE users SET profile_id = NULL"))
    
    # Remove profiles (cascade will handle relationships)
    connection.execute(sa.text("DELETE FROM user_profiles"))
```

### Safe Data Migrations

**REQUIRED**: Safe data migration patterns:

```python
def upgrade() -> None:
    """Safe data migration with validation."""
    connection = op.get_bind()
    
    # ✅ Good: Validate before migrating
    result = connection.execute(sa.text("SELECT COUNT(*) FROM users"))
    user_count = result.scalar()
    
    if user_count == 0:
        # No data to migrate
        return
    
    # ✅ Good: Migrate in batches for large datasets
    batch_size = 1000
    offset = 0
    
    while True:
        result = connection.execute(sa.text(f"""
            SELECT id FROM users
            LIMIT {batch_size} OFFSET {offset}
        """))
        user_ids = [row[0] for row in result]
        
        if not user_ids:
            break
        
        # Process batch
        for user_id in user_ids:
            connection.execute(sa.text(f"""
                INSERT INTO user_profiles (user_id, created_at, updated_at)
                VALUES ({user_id}, NOW(), NOW())
            """))
        
        offset += batch_size
    
    # ✅ Good: Verify migration
    result = connection.execute(sa.text("SELECT COUNT(*) FROM user_profiles"))
    profile_count = result.scalar()
    
    if profile_count != user_count:
        raise Exception(f"Migration failed: {profile_count} != {user_count}")
```

---

## Version Control

### Migration Naming Conventions

**REQUIRED**: Consistent naming:

```python
# ✅ Good: Descriptive revision IDs
revision = '001_initial_schema'
revision = '002_add_user_profiles'
revision = '003_add_email_verification'
revision = '004_migrate_legacy_data'

# ✅ Good: Clear messages
alembic revision --autogenerate -m "Add user profiles table"
alembic revision --autogenerate -m "Add email verification columns"
alembic revision -m "Migrate legacy user data to new schema"

# ❌ Bad: Vague names
revision = 'abc123'
revision = 'update'
```

### Migration History Management

**REQUIRED**: Track migration history:

```bash
# View migration history
alembic history

# View current revision
alembic current

# View pending migrations
alembic heads

# Check for multiple heads (branches)
alembic heads
# Should show single head in production
```

---

## Rollback Strategies

### Safe Rollback Patterns

**REQUIRED**: Rollback implementation:

```python
def downgrade() -> None:
    """Safe rollback with data preservation."""
    connection = op.get_bind()
    
    # ✅ Good: Backup data before rollback
    connection.execute(sa.text("""
        CREATE TABLE user_profiles_backup AS
        SELECT * FROM user_profiles
    """))
    
    # ✅ Good: Remove foreign key constraints first
    op.drop_constraint('fk_users_profile', 'users', type_='foreignkey')
    
    # ✅ Good: Drop dependent objects
    op.drop_index('idx_user_profiles_user_id', 'user_profiles')
    
    # ✅ Good: Drop table
    op.drop_table('user_profiles')
    
    # Note: Backup table remains for manual recovery if needed

def upgrade() -> None:
    """Restore from backup if needed."""
    connection = op.get_bind()
    
    # Check if backup exists
    result = connection.execute(sa.text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'user_profiles_backup'
        )
    """))
    
    if result.scalar():
        # Restore from backup
        connection.execute(sa.text("""
            INSERT INTO user_profiles
            SELECT * FROM user_profiles_backup
        """))
```

### Rollback Commands

**REQUIRED**: Rollback operations:

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade 001_initial_schema

# Rollback to base (empty database)
alembic downgrade base

# Rollback with SQL preview
alembic downgrade -1 --sql
```

---

## Multi-Database Support

### Multiple Database Migrations

**RECOMMENDED**: Multi-database support:

```python
# alembic/env.py
def run_migrations_online() -> None:
    """Run migrations for multiple databases."""
    databases = {
        "primary": get_settings().database_url,
        "analytics": get_settings().analytics_database_url,
    }
    
    for db_name, db_url in databases.items():
        config.set_main_option("sqlalchemy.url", db_url)
        
        connectable = async_engine_from_config(...)
        
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()
```

---

## Testing Migrations

### Migration Testing

**REQUIRED**: Test migrations:

```python
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

def test_migration_upgrade_downgrade():
    """Test migration upgrade and downgrade."""
    # Create test database
    engine = create_engine("sqlite:///:memory:")
    
    # Run migrations up
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
    
    command.upgrade(alembic_cfg, "head")
    
    # Verify schema
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "user_profiles" in tables
    
    # Rollback
    command.downgrade(alembic_cfg, "-1")
    
    # Verify rollback
    tables = inspector.get_table_names()
    assert "user_profiles" not in tables
```

---

## CI/CD Integration

### CI/CD Migration Workflow

**REQUIRED**: CI/CD integration:

```yaml
# .github/workflows/migrations.yml
name: Database Migrations

on:
  pull_request:
    paths:
      - 'alembic/**'
      - 'app/models/**'

jobs:
  test-migrations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install alembic
      
      - name: Check for pending migrations
        run: |
          alembic check
      
      - name: Test migrations
        run: |
          alembic upgrade head
          alembic downgrade -1
          alembic upgrade head
```

---

## Production Deployment

### Production Migration Strategy

**REQUIRED**: Production deployment:

```python
# scripts/run_migrations.py
import asyncio
from alembic import command
from alembic.config import Config
from app.config import get_settings

async def run_production_migrations():
    """Run migrations in production."""
    settings = get_settings()
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    
    # Check current revision
    from alembic.script import ScriptDirectory
    script = ScriptDirectory.from_config(alembic_cfg)
    heads = script.get_revisions("heads")
    
    print(f"Current heads: {[h.revision for h in heads]}")
    
    # Upgrade to head
    command.upgrade(alembic_cfg, "head")
    print("Migrations completed successfully")

if __name__ == "__main__":
    asyncio.run(run_production_migrations())
```

### Migration Safety Checklist

**REQUIRED**: Production checklist:

```python
# ✅ Pre-deployment checks
# 1. Backup database
# 2. Test migrations on staging
# 3. Review migration SQL
# 4. Check for data loss risks
# 5. Verify rollback plan
# 6. Schedule maintenance window if needed
# 7. Monitor migration progress
# 8. Verify post-migration state
```

---

## Summary

### Key Takeaways

1. **Version Control**: All migrations in version control
2. **Review Autogenerate**: Always review autogenerated migrations
3. **Test Migrations**: Test upgrades and downgrades
4. **Data Safety**: Backup data before migrations
5. **Atomic Operations**: Use transactions
6. **Reversible**: Every upgrade has downgrade
7. **Documentation**: Clear migration messages
8. **CI/CD**: Automate migration testing

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14
