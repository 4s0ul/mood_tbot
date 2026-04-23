from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    bot_token: str = ""
    g_creds_path: Path = Path(".secrets/g_creds.json")
    g_spread_key: str = ""
    admin_tg_ids: list[int] = []

    @field_validator("admin_tg_ids", mode="before")
    @classmethod
    def parse_admin_tg_ids(cls, value: str | list[int]) -> list[int]:
        if isinstance(value, list):
            return value
        if not value:
            return []
        return [int(item.strip()) for item in value.split(",") if item.strip()]


settings = Settings()
