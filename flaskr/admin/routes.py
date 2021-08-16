from flask import render_template, session, url_for, flash, request
from werkzeug.utils import redirect
import datetime, time

from . import admin
from .. import db
from ..models import Task, User, Account, Server, Property, TransactionLog

API_ENDPOINT = "https://discord.com/api/v8"
CLIENT_ID = "767749360586326026"
CLIENT_SECRET = "B8JBIE949Ak5DZZ-6DsmD4mG20Rf1U_S"
REDIRECT_URI = "http://localhost:5000/discord/auth"


@admin.route("/delete_property", methods=["GET", "POST"])
def delete_property():
    code = request.args.get("property_id")
    property = Property.query.filter_by(id=int(code)).first()
    isAdmin = False

    for g in session["guilds"]:
        if g[2] and int(property.property_guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("Naughty! You are not allowed to delete this property! *tuts* ", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    db.session.delete(property)
    db.session.commit()
    return redirect(
        url_for("admin.properties_dashboard", guild=property.property_guild)
    )


@admin.route("/admin/delete_account", methods=["GET", "POST"])
def delete_account():
    code = request.args.get("account_id")
    account = Account.query.filter_by(id=int(code)).first()
    server = Server.query.filter_by(guild_id=account.account_guild_id).first()
    isAdmin = False
    guild = account.account_guild_id

    for g in session["guilds"]:
        if g[2] and int(account.account_guild_id) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("Naughty! You are not allowed to delete this account! *tuts* ", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    if account.account_user.user_main_account == account.id:
        new_account = Account(
            account_user_id=account.account_user.user_id,
            account_guild_id=server.guild_id,
            account_balance=server.starting_amount,
        )
        db.session.add(new_account)
        db.session.commit()

        account.account_user.user_main_account
        db.session.commit()

    db.session.delete(account)
    db.session.commit()
    return redirect(url_for("admin.accounts_dashboard", guild=guild))


@admin.route("/admin/delete-task", methods=["GET", "POST"])
def delete_task():
    id = request.args.get("task_id")

    task = Task.query.filter_by(id=int(id)).first()
    isAdmin = False

    for g in session["guilds"]:
        if g[2] and int(task.guild_id) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("Naughty! You are not allowed to delete this task! *tuts* ", "danger")
        return redirect(url_for("index.index"))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("admin.tasks_dashboard", guild=task.guild_id))


@admin.route("/admin-dashboard", defaults={"guild": None}, methods=["GET", "POST"])
@admin.route("/admin-dashboard/<guild>", methods=["GET", "POST"])
def admin_dashboard(guild):
    user = None
    if not session["logged_in"]:
        return redirect(url_for("login.index"))
    if not session["userid"]:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    isAdmin = False

    for g in session["guilds"]:
        if g[2] and int(guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("You're not an admin in this server.", "danger")
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    user_exists = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=guild
    ).first()
    if user_exists:
        user = user_exists
    else:
        inserting_account = Account(
            account_user_id=session["userid"], account_guild_id=guild
        )
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(
            user_id=session["userid"],
            user_email=session["email"],
            user_name=session["name"],
            user_associated_guild=guild,
            user_main_account=inserting_account.id,
        )
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    server = Server.query.filter_by(guild_id=guild).first()

    if request.method == "POST":
        max_accounts = request.form.get("max_accounts")
        banker_role = request.form.get("banker_role")
        currency = request.form.get("currency")
        starting_amount = request.form.get("starting_amount")

        server.max_accounts = max_accounts
        server.banker_role = banker_role
        server.currency = currency
        server.starting_amount = starting_amount
        db.session.commit()
        flash("You have updated the servers settings.", "success")

    return render_template(
        "admin_dashboard.html",
        user=user if user is not None else None,
        logged_in=session["logged_in"],
        server=server,
    )


@admin.route("/properties", defaults={"guild": None}, methods=["GET", "POST"])
@admin.route("/properties/<guild>", methods=["GET", "POST"])
def properties_dashboard(guild):
    user = None
    if not session["logged_in"]:
        return redirect(url_for("login.index"))
    if not session["userid"]:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    isAdmin = False

    for g in session["guilds"]:
        if g[2] and int(guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("You're not an admin in this server.", "danger")
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    user_exists = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=guild
    ).first()
    if user_exists:
        user = user_exists
    else:
        inserting_account = Account(
            account_user_id=session["userid"], account_guild_id=guild
        )
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(
            user_id=session["userid"],
            user_email=session["email"],
            user_name=session["name"],
            user_associated_guild=guild,
            user_main_account=inserting_account.id,
        )
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    server = Server.query.filter_by(guild_id=guild).first()
    properties = Property.query.filter_by(property_guild=guild)

    if request.method == "POST":
        if "edit_property_name" in request.form:
            property_id = request.form.get("edit_property_id")
            property_name = request.form.get("edit_property_name")
            property_value = request.form.get("edit_property_value")
            property_owner = request.form.get("edit_property_owner")

            property = Property.query.filter_by(id=property_id).first()

            property.property_name = property_name
            property.property_value = property_value
            property.property_owner_id = int(property_owner)

            db.session.commit()
            flash("You have edited the property.", "success")
            return redirect(url_for("admin.properties_dashboard", guild=guild))

        if "property_name" in request.form:
            property_name = request.form.get("property_name")
            property_value = request.form.get("property_value")
            property_owner = request.form.get("property_owner")

            property_exists = Property.query.filter_by(
                property_name=property_name
            ).first()
            if property_exists:
                flash("A property already exists with this name.", "danger")
                return redirect(url_for("admin.properties_dashboard", guild=guild))

            property_user = User.query.filter_by(user_id=property_owner).first()

            new_property = Property(
                property_name=property_name,
                property_value=property_value,
                property_owner_id=property_user.user_id if property_user else None,
                property_guild=guild,
            )
            db.session.add(new_property)
            db.session.commit()

            trans = TransactionLog(
                user_id=new_property.property_owner_id,
                description=f"Property transferred. Value: {server.currency}{new_property.property_value}",
            )
            db.session.add(trans)
            db.session.commit()

            flash("You have created a property.", "success")

    return render_template(
        "admin_properties.html",
        user=user if user is not None else None,
        logged_in=session["logged_in"],
        server=server,
        properties=properties,
        users=User.query.filter_by(user_associated_guild=guild),
    )


@admin.route("/bank-accounts", defaults={"guild": None}, methods=["GET", "POST"])
@admin.route("/bank-accounts/<guild>", methods=["GET", "POST"])
def accounts_dashboard(guild):
    user = None
    if not session["logged_in"]:
        return redirect(url_for("login.index"))
    if not session["userid"]:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    isAdmin = False

    for g in session["guilds"]:
        if g[2] and int(guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("You're not an admin in this server.", "danger")
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    user_exists = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=guild
    ).first()
    if user_exists:
        user = user_exists
    else:
        inserting_account = Account(
            account_user_id=session["userid"], account_guild_id=guild
        )
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(
            user_id=session["userid"],
            user_email=session["email"],
            user_name=session["name"],
            user_associated_guild=guild,
            user_main_account=inserting_account.id,
        )
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    server = Server.query.filter_by(guild_id=guild).first()
    accounts = Account.query.filter_by(account_guild_id=guild)

    if request.method == "POST":
        if "account_value" in request.form:
            account_value = request.form.get("account_value")
            account_id = request.form.get("edit_property_id")

            account = Account.query.filter_by(id=account_id).first()
            if not account:
                flash("That account does not exist.", "danger")
                return redirect(url_for("admin.accounts_dashboard", guild=guild))

            account.account_balance = account_value

            transaction = TransactionLog(
                user_id=account.account_user.id,
                description=f"Account balance set to {account_value}",
            )
            db.session.add(transaction)

            db.session.commit()

            flash("Account balance has been updated.", "success")

    return render_template(
        "admin_bank_accounts.html",
        user=user if user is not None else None,
        logged_in=session["logged_in"],
        server=server,
        users=User.query.filter_by(user_associated_guild=guild),
        accounts=accounts,
    )


@admin.route("/admin-tasks", defaults={"guild": None}, methods=["GET", "POST"])
@admin.route("/admin-tasks/<guild>", methods=["GET", "POST"])
def tasks_dashboard(guild):
    user = None
    if not session["logged_in"]:
        return redirect(url_for("login.index"))
    if not session["userid"]:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    isAdmin = False

    for g in session["guilds"]:
        if g[2] and int(guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("You're not an admin in this server.", "danger")
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session["guilds"],
            logged_in=session["logged_in"],
        )

    user_exists = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=guild
    ).first()
    if user_exists:
        user = user_exists
    else:
        inserting_account = Account(
            account_user_id=session["userid"], account_guild_id=guild
        )
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(
            user_id=session["userid"],
            user_email=session["email"],
            user_name=session["name"],
            user_associated_guild=guild,
            user_main_account=inserting_account.id,
        )
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    server = Server.query.filter_by(guild_id=guild).first()
    tasks = Task.query.filter_by(guild_id=guild)

    if request.method == "POST":
        if "task_type" in request.form:
            task_type = request.form.get("task_type")
            task_amount = request.form.get("task_amount")
            target_id = request.form.get("target_id")
            frequency = request.form.get("frequency")

            print(frequency, time.time())
            frequency_t = int(frequency) * 24 * 60 * 60
            print(frequency_t)
            now = time.time()
            next = now + int(frequency_t)
            print(next)
            dt_object = datetime.datetime.fromtimestamp(next)

            task = Task(
                type=task_type,
                target_id=target_id,
                amount=task_amount,
                frequency=frequency,
                guild_id=guild,
                next_due=dt_object.date(),
            )

            db.session.add(task)
            db.session.commit()

            flash("Account balance has been updated.", "success")

    return render_template(
        "admin_task_management.html",
        user=user if user is not None else None,
        logged_in=session["logged_in"],
        server=server,
        users=User.query.filter_by(user_associated_guild=guild),
        tasks=tasks,
    )
