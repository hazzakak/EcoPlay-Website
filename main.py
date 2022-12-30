# ECOPLAY
# An economy system which connects discord and a website to enable roleplay communities and other fun communities to have an economic system.

# Copyright (C) 2022, Harry Smith.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
# You may contact me via hazzakak@gmail.com

#!/usr/bin/env python

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, db

app = create_app()

app.secret_key = b""
app.config["SECRET_KEY"] = app.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///utils/economy.db"

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run()
