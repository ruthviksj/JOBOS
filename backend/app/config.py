"""Application settings. Reads from environment; safe local defaults."""

import os
from functools import lru_cache
from pathlib import Path


# Repo root = parent of backend/ (the JOBOS workspace root).
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    """JOBOS runtime settings.

    - JOBOS_ROOT:          the JOBOS workspace directory (holds MASTER/, PROFILES/, ...).
    - JOBOS_DATABASE_URL:  SQLAlchemy URL. Defaults to a local SQLite file (cost-free,
                           zero-config). Set to a Postgres URL for production per spec 49.
    """

    def __init__(self) -> None:
        self.jobos_root = Path(os.getenv("JOBOS_ROOT", str(BASE_DIR)))
        self.database_url = os.getenv(
            "JOBOS_DATABASE_URL", "sqlite:///" + str(BASE_DIR / "jobos.db")
        )
        self.log_dir = self.jobos_root / "LOGS"
        self.log_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
