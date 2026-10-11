# Spec: Profile Page

## Overview
Implements the real `/profile` page for Spendly, replacing the current placeholder string (`"Profile page — coming in Step 4"`). This is the first protected page in the app — the first route that requires a session to view. It gives a signed-in user a place to see their own account details (name, email, member-since date) alongside a lightweight summary of their expense activity (total spent, number of expenses recorded), using the `users` and `expenses` tables already created in Step 01 and populated by Step 02/seed data. It does not implement expense editing, listing, or account editing — those remain later steps.

## Depends on
- Step 01 — Database Setup (`users` and `expenses` tables, `get_db()`, `init_db()`, `seed_db()`)
- Step 02 — Registration (`session['user_id']` convention, `create_user()`)
- Step 03 — Login and Logout (session-aware navbar in `base.html`, `/logout`)

## Routes
- `GET /profile` — render the signed-in user's profile with account info and expense summary — logged-in only (redirect to `{{ url_for('login') }}` if `session.user_id` is not set)

## Database changes
No schema changes. Two new read-only helper functions in `database/db.py` (parameterised queries, no new tables):
- `get_user_by_id(user_id)` — `SELECT id, name, email, created_at FROM users WHERE id = ?` — returns a single row
- `get_expense_summary(user_id)` — `SELECT COUNT(*) AS count, COALESCE(SUM(amount), 0) AS total FROM expenses WHERE user_id = ?` — returns a single row with `count` and `total`

## Templates
- **Create:** `templates/profile.html` — extends `base.html`; shows name, email, "member since" date (formatted from `created_at`), and an expense summary (total spent, number of expenses recorded)
- **Modify:** none (`base.html`'s navbar already links to `{{ url_for('profile') }}` when logged in, from Step 03)

## Files to change
- `app.py` — replace the placeholder `/profile` route: check `session.get('user_id')`, redirect to `login` if absent, otherwise call `get_user_by_id()` and `get_expense_summary()` and render `profile.html`
- `database/db.py` — add `get_user_by_id(user_id)` and `get_expense_summary(user_id)`
- `static/css/style.css` — add styles for the profile page (account card, summary stats), using existing CSS variables

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (not touched in this step — no password display or editing)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Never hardcode URLs in templates — use `{{ url_for(...) }}`
- Keep `app.py` route thin — the session check and redirect may live in the route, but all SQL stays in `database/db.py`
- If `session.user_id` points to a user that no longer exists (edge case), treat it the same as logged-out: clear the session and redirect to `login`
- Do not add profile editing, password change, or account deletion in this step — out of scope
- Do not add a reusable `login_required` decorator in this step — the inline session check on `/profile` is sufficient; a shared decorator can be introduced later if more protected routes are added
- Do not implement `/expenses/add`, `/expenses/<id>/edit`, or `/expenses/<id>/delete` as part of this spec — they remain placeholder routes

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login` and does not leak any user data
- [ ] Logging in as the seeded demo user (`demo@spendly.com` / `demo123`) and visiting `/profile` shows their name, email, and a member-since date
- [ ] The profile page shows the correct expense count and total amount for the seeded demo user's 8 seeded expenses
- [ ] Registering a brand-new user and visiting `/profile` shows that user's own name/email and an expense summary of 0 expenses / 0.00 total (not the demo user's data)
- [ ] `templates/profile.html` extends `base.html` and contains no hardcoded URLs
- [ ] `/profile` no longer returns a raw placeholder string
- [ ] App starts without errors and existing routes (`/`, `/register`, `/login`, `/logout`, `/terms`, `/privacy`) are unaffected
