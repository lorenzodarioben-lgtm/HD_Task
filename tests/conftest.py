# tests/conftest.py
import pytest, pathlib
try:
    # If running inside the image (your code is /app/app)
    from app import create_app
except Exception:
    # If running directly from the workspace (top-level __init__.py)
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
