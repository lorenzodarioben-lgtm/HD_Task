from flask import Flask
import os

# 👇 relative imports so the package works inside the container
from .models import db, login_manager
from .routes import bp as routes_bp

def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_TIME_LIMIT=None,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
