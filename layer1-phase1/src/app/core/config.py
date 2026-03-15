"""
Application configuration management using Pydantic Settings.

Loads configuration from environment variables with type validation
and default values.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Layer1 Phase1"
    app_env: str = "development"
    debug: bool = False
    version: str = "0.1.0"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database
    database_url: Optional[str] = None
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "layer1_phase1"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # LLM (Week 3+)
    llm_provider: str = "openai"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Cost Tracking
    track_llm_costs: bool = True

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings: Application settings instance
    """
    return Settings()
