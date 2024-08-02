import os

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    secret_key: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    model_config = SettingsConfigDict(env_file=f"{ROOT_PATH}/.env")


settings = Settings()
