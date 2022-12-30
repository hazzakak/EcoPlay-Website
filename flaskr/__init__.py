# ECOPLAY
# An economy system which connects discord and a website to enable roleplay communities and other fun communities to have an economic system.

# Copyright (C) 2022, Harry Smith.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
# You may contact me via hazzakak@gmail.com

from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def page_not_found(e):
    user = None

    if session.get("userid"):
        from flaskr.models import User

        user = User.query.filter_by(id=session["userid"]).first()
    return (
        render_template(
            "error.html",
            user=user if user is not None else None,
            logged_in=session.get("logged_in"),
            message="This page was not found.",
        ),
        404,
    )


def page_forbidden(e):
    user = None

    if session.get("userid"):
        from flaskr.models import User

        user = User.query.filter_by(id=session["userid"]).first()
    return (
        render_template(
            "error.html",
            user=user if user is not None else None,
            logged_in=session.get("logged_in"),
            message="Forbidden Page",
        ),
        403,
    )


def page_error(e):
    user = None

    if session.get("userid"):
        from flaskr.models import User

        user = User.query.filter_by(id=session["userid"]).first()
    return (
        render_template(
            "error.html",
            user=user if user is not None else None,
            logged_in=session.get("logged_in"),
            message="There has been an error occur.",
        ),
        500,
    )


def create_app():

    app = Flask(__name__)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)
    app.register_error_handler(500, page_error)

    from .login import login as login_blueprint

    app.register_blueprint(login_blueprint)

    from .index import index as index_blueprint

    app.register_blueprint(index_blueprint)

    from .personal import personal as personal_blueprint

    app.register_blueprint(personal_blueprint)

    from .admin import admin as admin_blueprint

    app.register_blueprint(admin_blueprint)

    from .API import api as api_blueprint

    app.register_blueprint(api_blueprint)

    from .docs import docs as docs_blueprint

    app.register_blueprint(docs_blueprint)

    db.init_app(app)

    return app
