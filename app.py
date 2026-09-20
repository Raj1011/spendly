import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database.db import create_user, get_db, get_user_by_email, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key"  # dev-only placeholder, not for production

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        return render_template(
            "register.html", error="All fields are required.", name=name, email=email
        )

    if "@" not in email:
        return render_template(
            "register.html", error="Enter a valid email address.", name=name, email=email
        )

    if len(password) < 8:
        return render_template(
            "register.html",
            error="Password must be at least 8 characters.",
            name=name,
            email=email,
        )

    if password != confirm_password:
        return render_template(
            "register.html",
            error="Passwords do not match.",
            name=name,
            email=email,
        )

    duplicate_error = render_template(
        "register.html",
        error="An account with this email already exists.",
        name=name,
        email=email,
    )

    if get_user_by_email(email):
        return duplicate_error

    try:
        user_id = create_user(name, email, password)
    except sqlite3.IntegrityError:
        return duplicate_error

    session["user_id"] = user_id
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    invalid_credentials_error = render_template(
        "login.html", error="Invalid email or password.", email=email
    )

    if not email or not password:
        return invalid_credentials_error

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return invalid_credentials_error

    session["user_id"] = user["id"]
    flash("Welcome back!")
    return redirect(url_for("landing"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out!")
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
