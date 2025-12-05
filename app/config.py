"""Configuration management for the application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    secret_key: str = "dev-secret-key-change-in-production-min-32-chars-long"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    coingecko_api_url: str = "https://api.coingecko.com/api/v3"
    default_per_page: int = 10

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


# Global settings instance
settings = Settings()

