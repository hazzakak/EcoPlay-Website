import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)

    from .index import index as index_blueprint
    app.register_blueprint(index_blueprint)

    from .personal import personal as personal_blueprint
    app.register_blueprint(personal_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    db.init_app(app)

    return app
