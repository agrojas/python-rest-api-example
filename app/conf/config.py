import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV_ENV = "dev"
    environment: str = DEV_ENV
    title: str
    description: str
    version: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 1
    database_url: str
    version_prefix: str

    class Config:
        BASE_DIR = os.path.dirname(os.path.abspath("../.env"))
        env_file = os.path.join(BASE_DIR, ".env")
