import os
from flask import Flask
from flask_wtf import CSRFProtect
from .models import db, login_manager
from .routes import bp as routes_bp

csrf = CSRFProtect()  # init once, attach in create_app

def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    app.config.update(
        # use env vars in prod; fallbacks for local/dev
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_TIME_LIMIT=None,   # avoid token expiry during long sessions
        WTF_CSRF_ENABLED=True,      # can be set to False in tests
    )
    if test_config:
        app.config.update(test_config)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)             # enables CSRF across the app

    with app.app_context():
        db.create_all()

    # blueprints
    app.register_blueprint(routes_bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
