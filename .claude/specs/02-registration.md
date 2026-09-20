# Spec: Registration

## Overview
Implements real user registration for Spendly. Today `/register` (GET) only renders a static form (`templates/register.html`) with no backend behind it — submitting it does nothing. This step wires the form to `POST /register`, validates and persists a new user via `database/db.py`, hashes the password with `werkzeug`, and redirects into a session-authenticated state. This is the first step in the Spendly roadmap that creates real user data and establishes the session mechanism that `/login`, `/logout`, `/profile`, and expense CRUD will all depend on later.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`, `init_db()`, `seed_db()` already implemented in `database/db.py`)

## Routes
- `GET /register` — render the registration form — public (already implemented; unchanged)
- `POST /register` — validate input, create the user, start a session, redirect to `/login` — public

## Database changes
No schema changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already supports registration as defined in `.claude/specs/01-database-setup.md`. This step adds a new function to `database/db.py`:
- `create_user(name, email, password)` — hashes the password with `generate_password_hash` and inserts a row into `users` via a parameterized query; returns the new `user_id`. Must let the `sqlite3.IntegrityError` from the `email UNIQUE` constraint propagate so the route can catch it and show a "email already registered" error.
- `get_user_by_email(email)` — needed by the route to pre-check/display a friendly duplicate-email error instead of a raw SQL error (used before insert, or the insert's `IntegrityError` can be caught directly — implementer's choice, but one of the two paths must produce a clean user-facing message).

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — change `<form method="POST" action="/register">` to `<form method="POST" action="{{ url_for('register') }}">` (hardcoded path violates CLAUDE.md); keep existing `{% if error %}` block wired to the new validation errors; repopulate `name`/`email` field values on validation failure so the user doesn't retype everything.

## Files to change
- `app.py` — add `POST` to the `/register` route's methods, parse form data, call `database/db.py` helpers, set session on success, redirect to `/login`
- `database/db.py` — add `create_user()` and `get_user_by_email()`
- `templates/register.html` — fix hardcoded form action, repopulate fields on error

## Files to create
None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Never hardcode URLs in templates — use `{{ url_for(...) }}`
- Keep `app.py` route thin — validation of required fields can live in the route, but all SQL stays in `database/db.py`
- Use `flask.session` for the logged-in state (Flask's built-in signed cookie session — no new package needed); store `user_id` in the session on successful registration
- Validate server-side: `name`, `email`, `password` all required and non-empty; email must contain `@`; password minimum 8 characters (matches the existing placeholder text "Min. 8 characters" in the template)
- On duplicate email, re-render `register.html` with an `error` message and HTTP 200 (not a redirect) — do not leak whether the failure was duplicate-email vs. something else in a way that reveals DB internals
- `/login` remains a stub for this step — redirecting a newly registered user there is expected to hit the existing placeholder string response; do not implement `/login` as part of this spec

## Definition of done
- [ ] `GET /register` still renders the form unchanged
- [ ] Submitting the form with valid name/email/password (≥8 chars) creates a row in the `users` table with a hashed (not plaintext) password
- [ ] After successful registration, the browser is redirected and a session cookie is set (verify `session['user_id']` is populated)
- [ ] Submitting with an email that already exists in `users` re-renders `register.html` with a visible error message and does not create a duplicate row
- [ ] Submitting with a missing field (name, email, or password) re-renders `register.html` with a visible error message and does not create a row
- [ ] Submitting with a password under 8 characters re-renders `register.html` with a visible error message and does not create a row
- [ ] `templates/register.html` contains no hardcoded `/register` path — form action uses `{{ url_for('register') }}`
- [ ] App starts without errors and existing routes (`/`, `/login`, `/terms`, `/privacy`) are unaffected
