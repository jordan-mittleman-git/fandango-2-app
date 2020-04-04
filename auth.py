import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for



from flask_app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


#Checks if a user id is stored in the session and gets that user’s data from the database,
#storing it on g.user, which lasts for the length of the request.
@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM RegUser WHERE user_id = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user. Validates that the user_id is not already taken."""
    if request.method == "POST":
        name = request.form["name"]
        user_id = request.form["user_id"]
        email = request.form["email"]
        phone = request.form["phone"]
        db = get_db()
        error = None

        if not name or not user_id or not email or not phone:
            error = "All fields must be filled."
        elif (
            db.execute("SELECT user_id FROM RegUser WHERE user_id = ?", (user_id,)).fetchone()
            is not None
        ):
            error = "User {0} is already registered.".format(user_id)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "INSERT INTO RegUser (name, user_id, email, phone) VALUES (?, ?, ?, ?)",
                (name, user_id, email, phone),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        user_id = request.form["user_id"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM RegUser WHERE user_id = ?", (user_id,)
        ).fetchone()

        if user is None:
            error = "Incorrect user_id"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
