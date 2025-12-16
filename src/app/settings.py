from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="WES_",
        env_file=".env",
        extra="ignore",
    )

    env: str = "dev"
    service_name: str = "p9-wes"
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://smt_mes_user:changeme123@localhost:5432/wes"
    redis_url: str = "redis://localhost:6379/0"
    wms_base_url: str = "http://localhost:8080"

    api_cors_origins: list[str] = ["*"]

    auto_create_db: bool = True
    strict_startup: bool = False
