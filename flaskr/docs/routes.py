from flask import render_template, session

from . import docs
from ..models import User


@docs.route("/docs", methods=["GET", "POST"])
def docs():
    user = None

    if session.get("userid"):
        user = User.query.filter_by(id=session["userid"]).first()
    return render_template(
        "coming_soon.html",
        user=user if user is not None else None,
        logged_in=session.get("logged_in"),
    )
