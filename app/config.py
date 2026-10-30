from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):

    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        env_file_encoding="utf-8",)


settings = Settings()
