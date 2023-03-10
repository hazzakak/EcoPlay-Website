# ECOPLAY
# An economy system which connects discord and a website to enable roleplay communities and other fun communities to have an economic system.

# Copyright (C) 2022, Harry Smith.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
# You may contact me via hazzakak@gmail.com

import requests
from flask import request, render_template, flash, session, url_for
from werkzeug.utils import redirect
import os

from . import login
from ..models import User, Server

API_ENDPOINT = "https://discord.com/api/v8"
CLIENT_ID = ""
CLIENT_SECRET = ""


if os.environ.get("FLASK_ENV") == "production" or os.environ.get("FLASK_ENV") == None:
    url = "https://discord.com/api/oauth2/authorize?client_id=767749360586326026&redirect_uri=https%3A%2F%2Fecoplay.xyz%2Fdiscord%2Fauth&response_type=code&scope=identify%20email%20guilds"
    REDIRECT_URI = "https://ecoplay.xyz/discord/auth"
elif os.environ.get("FLASK_ENV") == "development":
    REDIRECT_URI = "http://localhost:5000/discord/auth"
    url = "https://discord.com/api/oauth2/authorize?client_id=767749360586326026&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fdiscord%2Fauth&response_type=code&scope=identify%20email%20guilds"


@login.route("/login", methods=["GET", "POST"])
def index():
    user = None
    if session.get("userid"):
        user = User.query.filter_by(user_id=session.get("userid")).first()
    return render_template(
        "login.html",
        user=user if user is not None else None,
        logged_in=session.get("logged_in"),
        url=url,
    )


@login.route("/discord/auth", methods=["GET", "POST"])
def discordlogin():
    code = request.args.get("code")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify email connections",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("%s/oauth2/token" % API_ENDPOINT, data=data, headers=headers)

    if r.status_code != 200:
        flash("Error: could not connect to discord", "danger")
        return redirect(url_for("login.index"))

    r = r.json()

    s = requests.get(
        "https://discord.com/api/v8/users/@me",
        headers={"Authorization": "Bearer " + r["access_token"]},
    )
    if s.status_code != 200:
        flash("Error: could not connect get user", "danger")
        return redirect(url_for("login.index"))

    s = s.json()

    t = requests.get(
        "https://discord.com/api/v8/users/@me/guilds",
        headers={"Authorization": "Bearer " + r["access_token"]},
    )

    guilds_list = []
    for i in t.json():
        server = Server.query.filter_by(guild_id=i["id"]).first()
        if server:
            v = requests.get(
                f"https://discord.com/api/v8/guilds/{i['id']}/members/{s['id']}",
                headers={
                    "Authorization": "Bot "
                    + ""
                },
            )

            v = v.json()
            guilds_list.append(
                [
                    i["name"],
                    i["id"],
                    True if int(i["permissions"]) & 8 == 8 else False,
                    str(server.banker_role) in v["roles"] if "roles" in v else [],
                ]
            )

    session["guilds"] = guilds_list
    session["name"] = s["username"] + "#" + s["discriminator"]
    session["userid"] = s["id"]
    session["logged_in"] = True
    session["email"] = s["email"]

    flash(
        "Logged in succesfully, welcome "
        + s["username"]
        + "#"
        + s["discriminator"]
        + ".",
        "success",
    )
    return redirect(url_for("index.index"))


@login.route("/logout", methods=["GET", "POST"])
def logout():
    session["userid"] = None
    session["logged_in"] = False
    session["name"] = None
    session["owner_pass"] = False

    return redirect(url_for("index.index"))
