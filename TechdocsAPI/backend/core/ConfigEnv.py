"""Config class for handling env variables.
"""
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    HOSTNAME: str
    DATABASE: str
    UID: str
    PASSWORD: str
    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_VERIFICATION_SECRET_KEY: str
    APP_ID: str
    USER_ID: str
    MODEL_ID: str
    CLARIFAI_PAT: str
    MODEL_VERSION_ID: str

    MAIL_SERVER_URL:str
    
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    
    class Config:
        env_file = '.env'

@lru_cache()
def get_settings():
    """
    Returns the settings object.

    This function returns a settings object of the type Settings. This object contains various configuration
    settings used throughout the application.

    Returns:
    Settings: The settings object.
    """
    return Settings()
config = get_settings()