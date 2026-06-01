"""from typing import Optional

from pydantic import BaseSettings, PostgresDsn, RedisDsn, validator


class Config(BaseSettings):
    bot_token: str
    bot_fsm_storage: str
    postgres_dsn: PostgresDsn
    redis_dsn: Optional[RedisDsn]
    custom_bot_api: Optional[str]
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    webhook_domain: Optional[str]
    webhook_path: Optional[str]

    @validator("bot_fsm_storage")
    def validate_bot_fsm_storage(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis")
        return v

    @validator("redis_dsn")
    def validate_redis_dsn(cls, v, values):
        if values["bot_fsm_storage"] == "redis" and not v:
            raise ValueError("Redis DSN string is missing!")
        return v

    @validator("webhook_path")
    def validate_webhook_path(cls, v, values):
        if values["webhook_domain"] and not v:
            raise ValueError("Webhook path is missing!")
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Config()
"""

from pathlib import Path
from typing import Optional
from pydantic import model_validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.networks import PostgresDsn, RedisDsn


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        #env_file=Path(__file__).parent / '.env',
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__'
    )

    bot_token: str
    bot_fsm_storage: str
    postgres_dsn: PostgresDsn
    redis_dsn: Optional[RedisDsn] = None
    custom_bot_api: Optional[str] = None
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    webhook_domain: Optional[str] = None
    webhook_path: Optional[str] = None

    @field_validator("bot_fsm_storage")
    @classmethod
    def validate_bot_fsm_storage(cls, v: str) -> str:
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect 'bot_fsm_storage' value. Must be one of: memory, redis")
        return v

    @model_validator(mode="after")
    def validate_redis_and_webhook(self) -> "Config":
        if self.bot_fsm_storage == "redis" and not self.redis_dsn:
            raise ValueError("Redis DSN string is missing!")
        if self.webhook_domain and not self.webhook_path:
            raise ValueError("Webhook path is missing!")
        return self


config = Config()