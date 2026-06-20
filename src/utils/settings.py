"""Project-wide settings. Loads .env once at import time, then reads os.environ."""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, model_validator


load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)


class Settings(BaseModel):
    anthropic_api_key: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str = "openrouter/free"
    google_api_key: str | None = None
    google_model: str = "gemma-4-31b-it"
    google_timeout_ms: int = 120_000

    @model_validator(mode="before")
    @classmethod
    def _from_env(cls, data: object) -> object:
        if isinstance(data, dict) and data:
            return data
        return {
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY"),
            "openrouter_api_key": os.environ.get("OPENROUTER_API_KEY"),
            "openrouter_model": os.environ.get("OPENROUTER_MODEL", "openrouter/free"),
            "google_api_key": os.environ.get("GOOGLE_API_KEY"),
            "google_model": os.environ.get("GOOGLE_MODEL", "gemma-4-31b-it"),
            "google_timeout_ms": int(os.environ.get("GOOGLE_TIMEOUT_MS", "120000")),
        }
