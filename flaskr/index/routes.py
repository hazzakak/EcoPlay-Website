from flask import render_template, session

from . import index
from ..models import User


@index.route("/", methods=["GET", "POST"])
@index.route("/home", methods=["GET", "POST"])
def index():
    user = None

    if session.get("userid"):
        user = User.query.filter_by(id=session["userid"]).first()
    return render_template(
        "index.html",
        user=user if user is not None else None,
        logged_in=session.get("logged_in"),
    )
