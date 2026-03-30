from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = ""
    g_creds_path: Path = Path(".secrets/g_creds.json")
    g_spread_key: str = ""


settings = Settings()
