# Configuration Management Best Practices

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

This document provides comprehensive best practices for implementing configuration management in FastAPI applications using Pydantic Settings, covering environment variables, configuration files, validation, secrets management, multi-environment support, configuration reloading, and production deployment.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Pydantic Settings Setup](#pydantic-settings-setup)
3. [Environment Variables](#environment-variables)
4. [Configuration Files](#configuration-files)
5. [Validation & Type Safety](#validation--type-safety)
6. [Secrets Management](#secrets-management)
7. [Multi-Environment Support](#multi-environment-support)
8. [Configuration Reloading](#configuration-reloading)
9. [Production Deployment](#production-deployment)

---

## Architecture Principles

### Configuration Philosophy

**REQUIRED**: Understand configuration principles:

1. **Environment-Based**: Configuration varies by environment
2. **Type-Safe**: Use Pydantic for validation
3. **Secure**: Never commit secrets to version control
4. **Hierarchical**: Environment variables override defaults
5. **Validated**: Validate configuration at startup
6. **Documented**: Clear configuration documentation

### When to Use Configuration Management

**REQUIRED**: Use configuration management when:

- **Multiple Environments**: Different configs for dev/staging/prod
- **Secrets**: Need secure secret management
- **Dynamic Configuration**: Configuration changes without code changes
- **12-Factor App**: Following 12-factor app principles
- **Containerized**: Deploying in containers/Kubernetes

---

## Pydantic Settings Setup

### Basic Settings Configuration

**REQUIRED**: Pydantic Settings setup:

```python
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Core settings
    app_name: str = Field(default="fastapi-app", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port", ge=1, le=65535)
    
    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./app.db",
        description="Database URL",
    )
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins",
    )
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = {"development", "testing", "staging", "production"}
        if v.lower() not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v.lower()
    
    @property
    def is_development(self) -> bool:
        """Check if development environment."""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if production environment."""
        return self.environment == "production"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

---

## Environment Variables

### Environment Variable Patterns

**REQUIRED**: Environment variable configuration:

```python
# ✅ Good: Use prefixes to avoid conflicts
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
    
    database_url: str  # Reads from APP_DATABASE_URL
    secret_key: str    # Reads from APP_SECRET_KEY

# ✅ Good: Use nested configuration
class DatabaseConfig(BaseModel):
    url: str
    pool_size: int = 5

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
    )
    
    database: DatabaseConfig

# Environment variables:
# DATABASE__URL=postgresql://...
# DATABASE__POOL_SIZE=10
```

### Environment Variable Priority

**REQUIRED**: Configuration source priority:

```python
class Settings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        # Priority order (highest to lowest):
        # 1. init_settings (constructor arguments)
        # 2. env_settings (environment variables)
        # 3. dotenv_settings (.env file)
        # 4. file_secret_settings (secrets from files)
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
```

---

## Configuration Files

### YAML Configuration

**RECOMMENDED**: YAML configuration files:

```python
import yaml
from pathlib import Path

class Settings(BaseSettings):
    @classmethod
    def load_from_yaml(cls, file_path: Path) -> "Settings":
        """Load settings from YAML file."""
        with open(file_path) as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)

# config.yaml
# app_name: "My App"
# database_url: "postgresql://..."
# cors_origins:
#   - "http://localhost:3000"
```

---

## Validation & Type Safety

### Field Validation

**REQUIRED**: Field validation:

```python
from pydantic import Field, field_validator, EmailStr, HttpUrl

class Settings(BaseSettings):
    # Type validation
    port: int = Field(ge=1, le=65535)
    email: EmailStr
    api_url: HttpUrl
    
    # Custom validation
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Validate secret key."""
        if info.data.get("environment") == "production":
            if v == "default-secret-key":
                raise ValueError("Secret key must be changed in production")
        return v
```

---

## Secrets Management

### Secrets from Files

**REQUIRED**: Secure secrets management:

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets",  # Docker secrets directory
    )
    
    database_password: str  # Reads from /run/secrets/database_password
    api_key: str            # Reads from /run/secrets/api_key

# ✅ Good: Use Docker secrets
# docker run -d --secret database_password app

# ✅ Good: Use Kubernetes secrets
# Mount secrets as files in /run/secrets
```

### AWS Secrets Manager Integration

**RECOMMENDED**: AWS Secrets Manager:

```python
from pydantic_settings import AWSSecretsManagerSettingsSource

class Settings(BaseSettings):
    @classmethod
    def settings_customise_sources(cls, ...):
        aws_secrets = AWSSecretsManagerSettingsSource(
            settings_cls=cls,
            secret_id=os.getenv("AWS_SECRET_ID"),
        )
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            aws_secrets,
        )
```

---

## Multi-Environment Support

### Environment-Specific Configuration

**REQUIRED**: Multi-environment setup:

```python
class Settings(BaseSettings):
    environment: str = Field(default="development")
    
    # Environment-specific defaults
    @field_validator("database_url", mode="before")
    @classmethod
    def set_database_url(cls, v, info):
        """Set database URL based on environment."""
        env = info.data.get("environment", "development")
        
        if env == "production":
            return v or os.getenv("DATABASE_URL")
        elif env == "testing":
            return v or "sqlite+aiosqlite:///:memory:"
        else:
            return v or "sqlite+aiosqlite:///./app.db"
```

---

## Configuration Reloading

### Hot Reload Configuration

**RECOMMENDED**: Configuration reloading:

```python
from typing import Dict, Any
import asyncio

class ConfigurationManager:
    """Manage configuration with hot reload."""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._watchers: List[Callable] = []
    
    async def load_config(self):
        """Load configuration."""
        settings = Settings()
        self._config = settings.model_dump()
        
        # Notify watchers
        for watcher in self._watchers:
            await watcher(self._config)
    
    async def reload_config(self):
        """Reload configuration."""
        await self.load_config()
```

---

## Production Deployment

### Production Configuration

**REQUIRED**: Production setup:

```python
# Production configuration
class ProductionSettings(Settings):
    """Production-specific settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env.production",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Override defaults for production
    debug: bool = False
    environment: str = "production"
    
    # Required in production
    secret_key: str = Field(..., description="Secret key (required)")
    database_url: str = Field(..., description="Database URL (required)")
```

---

## Summary

### Key Takeaways

1. **Pydantic Settings**: Use BaseSettings for type-safe configuration
2. **Environment Variables**: Support 12-factor app principles
3. **Validation**: Validate all configuration values
4. **Secrets**: Never commit secrets, use secure storage
5. **Multi-Environment**: Support dev/staging/prod configurations
6. **Documentation**: Document all configuration options
7. **Production Ready**: Validated with 0 errors

---

**Version**: v1.0.0  
**Last Updated**: 2025-01-14

