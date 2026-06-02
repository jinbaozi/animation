from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    repo_root: Path = Path(__file__).resolve().parents[4]
    output_root: Path | None = None
    database_url: str = "sqlite:///./animation_workbench.db"

    model_config = SettingsConfigDict(env_prefix="ANIMATION_V3_")

    @property
    def resolved_output_root(self) -> Path:
        return self.output_root or self.repo_root / "output"


@lru_cache
def get_settings() -> Settings:
    return Settings()
