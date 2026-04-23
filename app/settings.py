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
    def parse_admin_tg_ids(cls, value: object) -> list[int]:
        if value is None:
            return []

        if isinstance(value, int):
            return [value]

        if isinstance(value, list):
            return [int(item) for item in value]

        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            return [int(item.strip()) for item in value.split(",") if item.strip()]

        raise TypeError(f"Unsupported admin_tg_ids value: {type(value)!r}")


settings = Settings()
