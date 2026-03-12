import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.infrastructure.config.grpcConfig import GrpcConfig
from src.infrastructure.config.dbConfig import DatabaseConfig
from src.infrastructure.config.loggerConfig import LoggerConfig


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_name = os.getenv("ENVIRONMENT", "development").lower()
env_file = BASE_DIR / f".env.{env_name}.local"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file= env_file,
        env_prefix="THEATER_SERVICE__",
        env_nested_delimiter="__"
    )
    db : DatabaseConfig = DatabaseConfig()
    logger : LoggerConfig = LoggerConfig()
    grpc: GrpcConfig = GrpcConfig()

settings = Settings()
