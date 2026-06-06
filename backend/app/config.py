"""
Config file to load environment variables from .env file and make them accessible throughout the app using the settings object
This way we can keep our sensitive information like database connection strings, API keys, etc. out of our codebase and easily manage them using environment variables.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get to where the .env file is located, whether the app is running in development or production, this way we can load the .env file correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
env_path = os.path.join(backend_dir, ".env")

class Settings(BaseSettings):
    # Pydantic will automatically read the MONGO_URL from the .env file and if dont find it will set it to None
    # So it doesnt crash the aplication
    MONGO_URL: Optional[str] = None
    

    # Set the config for Settings class to load .env and ignore extra fields (Security measures to prevent loading unwanted env variables that could be used for attacks)
    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Create an instance of the Settings class to access the .env values
settings = Settings()