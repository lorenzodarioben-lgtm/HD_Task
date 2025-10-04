# tests/conftest.py
import pytest
from pathlib import Path

try:
    # When running inside the container: your code is at /app/app
    from app import create_app
except Exception:
    # When running locally from the repo root: files are top-level
    from __init__ import create_app


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"
    cfg = {
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test-secret",
    }
    app = create_app(cfg)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
