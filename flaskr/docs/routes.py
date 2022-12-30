# ECOPLAY
# An economy system which connects discord and a website to enable roleplay communities and other fun communities to have an economic system.

# Copyright (C) 2022, Harry Smith.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
# You may contact me via hazzakak@gmail.com

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
