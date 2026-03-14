"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration for the omnimodal agent memory system."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    gemini_api_key: str = ""
    embedding_model: str = "gemini-embedding-2-preview"
    generation_model: str = "gemini-2.5-flash"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "agent_memory"

    data_dir: str = "data"
    max_file_size_mb: int = 20
    default_top_k: int = 5

    @property
    def vector_size(self) -> int:
        return 3072


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
