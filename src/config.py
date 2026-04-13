import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # LINE Bot Settings
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str

    # Google Drive Settings
    GOOGLE_DRIVE_FOLDER_ID: str
    
    # Path to the service account JSON file (for local development)
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # (Optional) Service account JSON content as a string (useful for Cloud Run env)
    GOOGLE_SERVICE_ACCOUNT_JSON: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
