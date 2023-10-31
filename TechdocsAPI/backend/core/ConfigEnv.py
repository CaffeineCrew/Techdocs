"""Config class for handling env variables.
"""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    HOSTNAME: str
    DATABASE: str
    UID: str
    PASSWORD: str
    ALGORITHM:str
    JWT_SECRET_KEY:str
    JWT_REFRESH_SECRET_KEY:str
    JWT_VERIFICATION_SECRET_KEY:str
    # OPENAI_KEY:str
    APP_ID:str
    USER_ID:str
    MODEL_ID:str
    CLARIFAI_PAT:str
    MODEL_VERSION_ID:str

    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


config = get_settings()
