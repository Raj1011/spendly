# Spec: Login and Logout

## Overview
Implements real authentication for Spendly. Today `/login` (GET) only renders a static form (`templates/login.html`) with no backend behind it, and `/logout` is a placeholder string. This step wires the login form to `POST /login`, verifies credentials against the `users` table created in Step 01 and populated by Step 02's registration flow, starts a session on success, and implements `/logout` to end that session. It also makes the navbar in `base.html` session-aware so a signed-in user has a visible way to sign out. This is the step that makes the session mechanism established in registration actually round-trip: register → login → logout.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`, `init_db()`, `seed_db()`)
- Step 02 — Registration (`create_user()`, `get_user_by_email()` in `database/db.py`; `session['user_id']` convention)

## Routes
- `GET /login` — render the login form — public (already implemented; unchanged)
- `POST /login` — validate credentials, start a session, redirect to `/profile` on success — public
- `GET /logout` — clear the session, redirect to `/` — logged-in (safe to hit while logged out too; it just clears an empty session and redirects)

## Database changes
No schema changes. `get_user_by_email(email)` already exists in `database/db.py` (from Step 02) and returns `id`, `name`, `email`, `password_hash` — sufficient for login. No new `database/db.py` functions are needed; password verification uses `werkzeug.security.check_password_hash` directly against the row returned by `get_user_by_email`, which is hash comparison, not SQL, so it belongs in the route.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — change `<form method="POST" action="/login">` to `<form method="POST" action="{{ url_for('login') }}">` (hardcoded path violates CLAUDE.md); add an `{% if error %}` block (mirroring `register.html`'s `auth-error` pattern) wired to invalid-credential errors; repopulate the `email` field value on failure.
  - `templates/base.html` — make the navbar session-aware: when `session.user_id` is not set, show the existing "Sign in" / "Get started" links; when it is set, show a link to `{{ url_for('profile') }}` and a "Sign out" link to `{{ url_for('logout') }}` instead.

## Files to change
- `app.py` — add `POST` to the `/login` route's methods, parse form data, validate, verify password with `check_password_hash`, set `session['user_id']` on success, redirect to `/profile`; implement `/logout` to clear the session and redirect to `/`
- `templates/login.html` — fix hardcoded form action, add error display, repopulate email on error
- `templates/base.html` — conditional nav based on `session.user_id`

## Files to create
None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` against the stored `password_hash`; never compare plaintext passwords)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Never hardcode URLs in templates — use `{{ url_for(...) }}`
- Keep `app.py` route thin — validation and `check_password_hash` calls may live in the route, but all SQL stays in `database/db.py`
- Use `flask.session` for the logged-in state (already established convention from Step 02); store `user_id` in the session on successful login
- Validate server-side: `email` and `password` both required and non-empty
- On missing user, wrong password, or missing fields, re-render `login.html` with a single generic error message (e.g. "Invalid email or password") and HTTP 200 — do not reveal whether the email exists or the password was wrong
- `/logout` must clear the session (`session.pop('user_id', None)` or `session.clear()`) and redirect — it must not render a template with sensitive state
- `/profile` remains a stub for this step — redirecting a successful login there is expected to hit the existing placeholder string response; do not implement `/profile` as part of this spec
- Do not add a `login_required` decorator or protect `/profile`/`/expenses/*` routes in this step — access control for those routes is out of scope here and belongs to a later step

## Definition of done
- [ ] `GET /login` still renders the form unchanged (plus the new conditional error block, empty by default)
- [ ] Submitting valid credentials for the seeded demo user (`demo@spendly.com` / `demo123`) redirects and sets `session['user_id']`
- [ ] Submitting valid credentials for a user created via `/register` in this session also succeeds
- [ ] Submitting a non-existent email re-renders `login.html` with a visible generic error and does not set a session
- [ ] Submitting an existing email with the wrong password re-renders `login.html` with a visible generic error and does not set a session
- [ ] Submitting with a missing email or password re-renders `login.html` with a visible error and does not set a session
- [ ] Visiting `/logout` after being logged in clears `session['user_id']` and redirects to `/`
- [ ] Visiting `/logout` while already logged out does not error and redirects to `/`
- [ ] `templates/login.html` contains no hardcoded `/login` path — form action uses `{{ url_for('login') }}`
- [ ] When logged in, the navbar shows a sign-out link instead of "Sign in" / "Get started"; when logged out, the original nav links are shown
- [ ] App starts without errors and existing routes (`/`, `/register`, `/terms`, `/privacy`) are unaffected
