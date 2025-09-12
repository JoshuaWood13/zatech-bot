from __future__ import annotations

from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Slack
    slack_bot_token: str = Field(alias="SLACK_BOT_TOKEN")
    slack_app_token: Optional[str] = Field(default=None, alias="SLACK_APP_TOKEN")
    slack_signing_secret: Optional[str] = Field(default=None, alias="SLACK_SIGNING_SECRET")

    # Mode: socket or http
    mode: Literal["socket", "http"] = Field(default="socket", alias="ZEBRAS_MODE")

    # HTTP server
    http_host: str = Field(default="0.0.0.0", alias="ZEBRAS_HTTP_HOST")
    http_port: int = Field(default=3000, alias="ZEBRAS_HTTP_PORT")

    # Redis / RQ
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # Database (Postgres). For Neon, paste your Neon DSN here
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/zebras",
        alias="DATABASE_URL",
    )

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


def load_settings() -> AppSettings:
    s = AppSettings()  # type: ignore[arg-type]
    # Honor generic PORT env var commonly set by PaaS (e.g., Coolify) if present
    port_env = os.getenv("PORT")
    if port_env:
        try:
            s.http_port = int(port_env)  # type: ignore[attr-defined]
        except ValueError:
            pass
    return s
