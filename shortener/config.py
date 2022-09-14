from functools import lru_cache

from pydantic import BaseSettings


class DBSettings(BaseSettings):
    username: str
    password: str
    name: str
    host: str
    port: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


@lru_cache
def get_db_settings() -> DBSettings:
    return DBSettings()


class Settings(BaseSettings):
    """
    Define environment variables in the application that should be used
    """
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = f"postgresql://{get_db_settings().username}:{get_db_settings().password}@{get_db_settings().host}:" \
                          f"{get_db_settings().port}/{get_db_settings().name}"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    Show a message in logs once the settings is loaded
    :return:
    An onstance of Settings class that is caching by lru_cache decorator
    """
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings

