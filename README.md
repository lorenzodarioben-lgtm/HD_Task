# Flask Shopping List — Pro Edition (Auth + CRUD, Bootstrap UI)

A clean, product-style **Flask + Jinja** web app with:
- **User authentication** (register, login, logout).
- **CRUD** for Shopping Lists and Items (quantity, priority, purchased toggle).
- **Modern UI** using **Bootstrap 5** + small custom CSS.
- **CSRF-protected forms** (Flask‑WTF).
- Health endpoint: `GET /health` → `{"status":"ok"}`.

> Next steps (optional): pytest tests, Docker/Compose, Prometheus metrics, Sonar/Bandit/Trivy, Jenkins pipeline.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app:create_app
export FLASK_ENV=development  # optional for auto-reload
flask run  # http://127.0.0.1:5000
```

### Create an account
1) Visit **/register**, create your user, then **/login**.
2) Make your first list and add items.

## Project structure
```
app/
  __init__.py
  models.py
  forms.py
  routes.py
  templates/
    base.html, macros.html, login.html, register.html, dashboard.html, list_detail.html
  static/
    site.css
requirements.txt
README.md
```
