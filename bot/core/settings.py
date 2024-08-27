from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from aiogram.enums import ParseMode


class ApiConfig(BaseModel):
    url: str


class BotConfig(BaseModel):
    token: str
    default_parse_mode: ParseMode = ParseMode.HTML


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="BOT_CONFIG__",
    )

    bot: BotConfig
    api: ApiConfig

settings = Settings()
