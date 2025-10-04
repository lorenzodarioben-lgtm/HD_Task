# tests/conftest.py
import os, sys, pathlib, pytest

# If running inside the container, code is at /app/app -> package name "app"
if os.getenv("CI_IN_CONTAINER") == "1":
    from app import create_app  # <-- container path
else:
    # Local dev fallback so `pytest` from repo root still works
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    try:
        from app import create_app       # if you've made a local 'app' package
    except Exception:
        from __init__ import create_app  # top-level files case

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
