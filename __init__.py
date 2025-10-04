from flask import Flask
import os

from .models import db, login_manager
from .routes import bp as routes_bp
# NEW: add CSRFProtect
from flask_wtf import CSRFProtect

csrf = CSRFProtect()  # NEW

def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_TIME_LIMIT=None,
        WTF_CSRF_ENABLED=True,  # default on; tests override to False
    )
    if test_config:
        app.config.update(test_config)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)  # NEW: register CSRF extension

    # When CSRF is disabled (tests), provide a dummy helper so templates don’t crash
    if not app.config.get("WTF_CSRF_ENABLED", True):  # NEW
        @app.context_processor
        def inject_csrf():  # NEW
            return dict(csrf_token=lambda: "")  # NEW

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
