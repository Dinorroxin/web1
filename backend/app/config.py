import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get to where the .env file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
env_path = os.path.join(backend_dir, ".env")

class Settings(BaseSettings):
    # Pydantic will automatically read the MONGO_URL from the .env file
    MONGO_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Create an instance of the Settings class to access the .env values
settings = Settings()