import sqlite3
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from database.db import (
    create_user,
    get_category_breakdown,
    get_db,
    get_expense_summary,
    get_recent_expenses,
    get_sample_profile_data,
    get_user_by_email,
    get_user_by_id,
    init_db,
    seed_db,
)

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
    return redirect(url_for("profile"))


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


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        return redirect(url_for("login"))

    summary = get_expense_summary(user_id)
    member_since = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y")

    if summary["count"]:
        data = {
            "total": summary["total"],
            "count": summary["count"],
            "transactions": get_recent_expenses(user_id),
            "categories": get_category_breakdown(user_id),
        }
        is_sample = False
    else:
        data = get_sample_profile_data()
        is_sample = True

    return render_template(
        "profile.html",
        user=user,
        member_since=member_since,
        is_sample=is_sample,
        total=data["total"],
        count=data["count"],
        top_category=data["categories"][0]["category"],
        transactions=data["transactions"],
        categories=data["categories"],
        max_category_total=data["categories"][0]["total"],
    )


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

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
