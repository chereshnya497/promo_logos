"""
Application configuration — reads from environment variables / .env file.
"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # AI backend selection
    AI_BACKEND: Literal["openai", "stable_diffusion"] = "openai"

    # OpenAI settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "dall-e-3"

    # Stable Diffusion settings (local)
    SD_API_URL: str = "http://localhost:7860"

    # Image defaults
    IMAGE_SIZE: str = "1024x1024"
    IMAGE_QUALITY: Literal["standard", "hd"] = "standard"
    MAX_LOGOS_PER_REQUEST: int = 5

    # Storage
    OUTPUT_DIR: str = "outputs"
    USE_S3: bool = False
    AWS_BUCKET: str = ""
    AWS_REGION: str = "us-east-1"

    # App
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
