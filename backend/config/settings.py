import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env from backend directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/agentbench"
    OPENAI_API_KEY: str = ""
    FUTUREAGI_API_KEY: str = ""
    FUTUREAGI_API_URL: str = "https://api.futureagi.com/v1/evaluate"

    class Config:
        env_file = str(env_path)


settings = Settings()
