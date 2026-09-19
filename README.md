# Expense Tracker

A simple Flask web app for tracking personal expenses.

## Requirements

- Python 3.9+
- pip

## Setup

1. Clone the repository and move into the project folder:

   ```bash
   git clone <repo-url>
   cd expense-tracker
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the app

```bash
python app.py
```

The app starts in debug mode on **http://localhost:5001**.

## Running tests

```bash
pytest
```

## Project structure

```
app.py                  # Flask app and routes
database/
  db.py                 # Database connection/setup helpers (get_db, init_db, seed_db)
templates/              # Jinja2 HTML templates (landing, login, register, base)
static/
  css/style.css
  js/main.js
requirements.txt
```

## Status

This project is a work in progress. Currently implemented:

- Landing, register, and login pages (`/`, `/register`, `/login`)

Not yet implemented (placeholder routes return a plain string):

- Logout, profile, and expense CRUD (`add`, `edit`, `delete`)
- Database layer (`database/db.py` is currently a stub)
