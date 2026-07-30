from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from typing import Literal

class Config(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str = "LedgerFlow"
    app_port: int = 8000

    env: Literal["prod","dev","test"] = "dev"

    better_stack_source_token: str 
    better_stack_host: str

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"

    @property
    def is_test(self) -> bool:
        return self.env == "test"

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"
        

@lru_cache(maxsize=128)
def get_config() -> Config:
    """
    This will return the config required for the application it will be cache at run_time using lru_cache
    """
    return Config()