from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def page_not_found(e):
    return render_template("error.html", message="This page was not found."), 404


def page_forbidden(e):
    return render_template("error.html", message="Forbidden Page"), 403


def page_error(e):
    return render_template("error.html", message="There has been an error occur."), 500


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
