from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # =========================
    # Application
    # =========================
    APP_NAME: str = "Hospital Billing System"
    DEBUG: bool = True

    # =========================
    # Database
    # =========================
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "hospital_db"

    DATABASE_URL: str | None = None

    # =========================
    # Security / JWT
    # =========================
    SECRET_KEY: str = "CHANGE_ME_SUPER_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    # Build DATABASE_URL dynamically if not provided
    if not settings.DATABASE_URL:
        settings.DATABASE_URL = (
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
            f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )

    return settings
