# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"Spendly" — a Flask-based personal expense tracker, built incrementally as a student project. It currently has landing/register/login/terms/privacy pages; auth, sessions, and expense CRUD are not yet implemented (see "Implemented vs. stub routes" below).

## Architecture

```
app.py                     # Flask app + ALL routes (no blueprints)
database/
  __init__.py              # empty (package marker)
  db.py                     # STUB — will hold get_db(), init_db(), seed_db()
templates/
  base.html                 # shared layout: navbar, footer, {% block content %}
  landing.html               # extends base.html
  login.html                 # extends base.html
  register.html               # extends base.html
  terms.html                 # extends base.html
  privacy.html                # extends base.html
static/
  css/style.css              # single global stylesheet
  js/main.js                 # single global script (currently empty/placeholder)
requirements.txt
README.md
```

## Where things belong

- **New page/route** → add a view function in `app.py`, add a matching template in `templates/` that extends `base.html`.
- **Database logic** (queries, schema, seed data) → `database/db.py` only, via `get_db()` / `init_db()` / `seed_db()`. Route functions call into these, they don't contain SQL themselves.
- **Shared layout elements** (nav, footer, fonts, global `<head>` tags) → `templates/base.html`.
- **Page-specific markup** → the page's own template, inside `{% block content %}`.
- **Styling** → `static/css/style.css`. There is one global stylesheet; no per-page CSS files.
- **Client-side behavior** → `static/js/main.js`. There is one global script; no per-page JS files, no bundler/build step.
- **Internal links in templates** → always `{{ url_for('endpoint_name') }}`, never a hardcoded path.

## Code Style

- Routes are plain `@app.route(...)` view functions in `app.py`, grouped under the `# Routes` / `# Placeholder routes` comment banners already present — keep new routes in the appropriate section.
- Templates use Jinja2 inheritance (`{% extends "base.html" %}` + `{% block content %}`); don't duplicate the `<html>/<head>/<nav>/<footer>` structure in individual page templates.
- Keep view functions thin: parse request → call `database/db.py` helpers → render a template or redirect. No inline SQL or business logic in `app.py`.

## Tech Constraints

- **Flask only** — no other web framework.
- **SQLite only** — no other database engine, no ORM (SQLAlchemy, etc.) unless explicitly requested.
- **Vanilla JS only** — no JS frameworks/libraries (React, Vue, jQuery, etc.), no build tooling.
- **No new pip packages** beyond what's in `requirements.txt` (`flask`, `werkzeug`, `pytest`, `pytest-flask`) unless the user explicitly asks for one.

## Commands

```bash
# Activate the venv first (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app (debug mode, http://localhost:5001)
python app.py

# Run tests
pytest
```

There is no lint/format tooling configured in this repo.

## Implemented vs. stub routes

Implemented (render real templates):
- `/` — landing
- `/register` — register form
- `/login` — login form
- `/terms` — terms and conditions
- `/privacy` — privacy policy

Stub (return a plain string placeholder, not yet built):
- `/logout`
- `/profile`
- `/expenses/add`
- `/expenses/<int:id>/edit`
- `/expenses/<int:id>/delete`

`database/db.py` is also a stub (docstring only) — implementing any stub route that needs persistence requires writing the corresponding piece of `db.py` first.

## Warnings and things to avoid

- Never hardcode URLs in templates — always use `{{ url_for(...) }}`.
- Never introduce a JS framework or client-side build step — this project is vanilla JS served as static files.
- Never put database/SQL logic directly inside route functions in `app.py` — it belongs in `database/db.py`.
- Never leave a newly implemented route returning a raw string — stub routes return plain strings as a *known, temporary* placeholder; once you implement a route, it must render a template (or redirect/JSON as appropriate), not a bare string.
- Never add a new pip dependency without explicit user approval.
- Never invent a database engine or ORM — SQLite via the stdlib `sqlite3` module (through `database/db.py`) is the only persistence layer.
