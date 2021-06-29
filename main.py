#!/usr/bin/env python

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app

app = create_app()

app.secret_key = b'9*awdka#wdkawpodjoaiw'
app.config["SECRET_KEY"] = app.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utils/main.db'


if __name__ == '__main__':
    app.run(debug=True)
