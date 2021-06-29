#!/usr/bin/env python

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, db

app = create_app()

app.secret_key = b'9*awdka#wdkawpodjoaiw'
app.config["SECRET_KEY"] = app.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utils/economy.db'

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
