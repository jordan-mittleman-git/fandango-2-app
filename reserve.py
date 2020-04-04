
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db

bp = Blueprint("reserve", __name__)



@bp.route("/")
@login_required
def index():
    """Display all the reservations that the user has made"""
    db = get_db()
    reservations = db.execute(
        "SELECT * FROM Listings WHERE user_id = ? ORDER BY date DESC", (g.user["user_id"],)
    ).fetchall()
    return render_template("index.html", reservations=reservations)


@bp.route("/makereservation", methods=("GET", "POST"))
@login_required
def make_reservation():
    """When the user wants to reserve a movie"""
    if request.method == "POST":
        #TO DO: Figure out how to let user click the listing they want to reserve (rather than type in info)? 
        movie_id = request.form["movie_id"]
        seat_number = request.form["seat_number"]
        room_number = request.form["room_number"]
        theater_addr = request.form["theater_addr"]
        time_slot = request.form["time_slot"]
        error = None
    
        checker = get_db().execute(
            "SELECT user_id FROM Listings"
            " WHERE movie_id = ? AND seat_number = ? AND room_number = ? AND theater_addr = ? AND time_slot = ?",
            (movie_id, seat_number, room_number, theater_addr, time_slot),
        ).fetchone()

        if checker:
            error = "Someone else has already reserved this listing"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE Lisings SET user_id = ?"
                " WHERE movie_id = ? AND seat_number = ? AND room_number = ? AND theater_addr = ? AND time_slot = ?",
                (user_id, movie_id, seat_number, room_number, theater_addr, time_slot),
            )
            db.commit()
            return redirect(url_for("reserve.index"))

    return render_template("makereservation.html")






