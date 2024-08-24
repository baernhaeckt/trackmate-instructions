import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = os.environ.get("ENV", default="development")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")


# Init the settings of the application on startup
load_dotenv()
settings: Settings = Settings()
