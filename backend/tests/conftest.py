"""Test isolation: fresh temp DB per run, seeded once.

Set JOBOS_DATABASE_URL before app.config is first imported so the whole app
(engine, SessionLocal) binds to an isolated database. Seed it for tests that
need profiles/evidence.
"""

import os
import tempfile

_fd, _path = tempfile.mkstemp(suffix=".db", prefix="jobos_test_")
os.close(_fd)
os.environ["JOBOS_DATABASE_URL"] = f"sqlite:///{_path}"

import pytest  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _seeded_db():
    from app.seed import seed

    seed()
    yield
    try:
        os.remove(_path)
    except OSError:
        pass
