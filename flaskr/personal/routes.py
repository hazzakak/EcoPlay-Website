from flask import render_template, session, url_for, request, flash
from werkzeug.utils import redirect

from . import personal
from .. import db
from ..models import User, Account, Property, Server, TransactionLog

API_ENDPOINT = "https://discord.com/api/v8"
CLIENT_ID = "767749360586326026"
CLIENT_SECRET = "B8JBIE949Ak5DZZ-6DsmD4mG20Rf1U_S"
REDIRECT_URI = "http://localhost:5000/discord/auth"


@personal.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    code = request.args.get("account_id")
    account = Account.query.filter_by(id=int(code)).first()
    if int(account.account_user_id) != int(session["userid"]):
        flash("Naughty! This is not your account to delete! *tuts* ", "danger")
        return redirect(url_for("personal.pers_dashboard"))

    user = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=account.account_guild_id
    ).first()
    main_account = Account.query.filter_by(id=user.user_main_account).first()

    if account.id == main_account.id:
        flash(
            "You sadly cannot delete your debts away, you need to keep your main account.",
            "danger",
        )
        return redirect(
            url_for("personal.pers_dashboard", guild=account.account_guild_id)
        )

    main_account.account_balance += account.account_balance
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for("personal.pers_dashboard", guild=account.account_guild_id))


@personal.route("/make_default_account", methods=["GET", "POST"])
def make_default_account():
    code = request.args.get("account_id")
    account = Account.query.filter_by(id=int(code)).first()
    if int(account.account_user_id) != int(session["userid"]):
        flash("Naughty! This is not your account to delete! *tuts* ", "danger")
        return redirect(url_for("personal.pers_dashboard"))

    user = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=account.account_guild_id
    ).first()
    user.user_main_account = account.id

    db.session.commit()
    return redirect(url_for("personal.pers_dashboard", guild=account.account_guild_id))


@personal.route("/purchase-property", methods=["GET", "POST"])
def purchase_property():
    id = request.args.get("id")
    guild = request.args.get("guild")

    property = Property.query.filter_by(id=int(id)).first()
    guild = guild.replace(" ", "")
    if property.property_guild != int(guild):
        print(2, guild)
        return redirect(url_for("personal.pers_dashboard"))

    user = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=int(guild)
    ).first()
    if not user:
        print(1)
        return redirect(url_for("personal.pers_dashboard"))

    account = Account.query.filter_by(id=user.user_main_account).first()
    if account.account_balance < property.property_value:
        flash("You do not have enough money in your main account.", "danger")
        return redirect(url_for("personal.pers_dashboard", guild=guild))

    property.property_owner_id = user.user_id
    account.account_balance -= property.property_value

    db.session.commit()

    print(guild)

    flash("You have successfully purchased the property.", "success")
    return redirect(url_for("personal.pers_dashboard", guild=guild))


@personal.route(
    "/personal-dashboard", defaults={"guild": None}, methods=["GET", "POST"]
)
@personal.route("/personal-dashboard/<guild>", methods=["GET", "POST"])
def pers_dashboard(guild):
    user = None
    if not session.get("logged_in"):
        return redirect(url_for("login.index"))
    if not session.get("userid"):
        return redirect(url_for("login.index"))

    if not guild:
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session.get("guilds"),
            logged_in=session.get("logged_in"),
        )

    user_exists = User.query.filter_by(
        user_id=session.get("userid"), user_associated_guild=guild
    ).first()
    if user_exists:
        user = user_exists
        user.user_email = session.get("email")
        db.session.commit()
    else:
        inserting_account = Account(
            account_user_id=session.get("userid"), account_guild_id=guild
        )
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(
            user_id=session.get("userid"),
            user_email=session.get("email"),
            user_name=session.get("name"),
            user_associated_guild=guild,
            user_main_account=inserting_account.id,
        )
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    main_account = Account.query.filter_by(id=user.user_main_account).first()
    properties = Property.query.filter_by(
        property_guild=guild, property_owner_id=user.user_id
    ).all()
    accounts = Account.query.filter_by(
        account_user_id=session.get("userid"), account_guild_id=guild
    )
    server = Server.query.filter_by(guild_id=guild).first()
    networth = 0

    for p in properties:
        networth += p.property_value

    for a in accounts:
        networth += a.account_balance

    if request.method == "POST":
        if "account_name" in request.form:
            account_name = request.form.get("account_name")
            inserting_account = Account(
                account_user_id=session.get("userid"),
                account_guild_id=guild,
                account_name=account_name,
                account_balance=0,
            )
            db.session.add(inserting_account)
            db.session.commit()

        if "account_from" in request.form:
            account_from = request.form.get("account_from")
            account_to = request.form.get("account_to")
            amount = request.form.get("amount")

            account_from = Account.query.filter_by(id=account_from).first()
            account_to = Account.query.filter_by(id=account_to).first()

            if account_from == None or account_to == None:
                return redirect(url_for("personal.pers_dashboard", guild=guild))

            if account_from.account_user_id != user.user_id:
                flash(
                    "SO CLOSE! But yet so far. Give up messing about with my website - best dev ever.",
                    "danger",
                )
                return redirect(url_for("personal.pers_dashboard", guild=guild))

            if (
                not account_to
                or account_to.account_guild_id != user.user_associated_guild
            ):
                flash("That account does not exist ;(", "danger")
                return redirect(url_for("personal.pers_dashboard", guild=guild))

            if account_from.account_balance < int(amount):
                flash("You don't have enough money for that!", "danger")
                return redirect(url_for("personal.pers_dashboard", guild=guild))

            account_from.account_balance -= int(amount)
            account_to.account_balance += int(amount)

            db.session.commit()

            transaction = TransactionLog(
                user_id=account_from.account_user.id,
                description=f"Transfered {server.currency}{amount} from {account_from.id} to {account_to.id}",
            )
            db.session.add(transaction)

            db.session.commit()

            flash(
                f"Successfully sent {server.currency}{amount} to account number {account_to.id} from your account {account_from.id}.",
                "success",
            )
            return redirect(url_for("personal.pers_dashboard", guild=guild))
        if "property_name" in request.form:
            print(1)
            property_id = request.form.get("property_name")
            new_owner = request.form.get("property_owner")

            user = User.query.filter_by(
                user_id=int(new_owner), user_associated_guild=guild
            ).first()
            property = Property.query.filter_by(id=property_id).first()

            if not user:
                print(2)
                return redirect(url_for("personal.pers_dashboard", guild=guild))
            if not property:
                print(3)
                return redirect(url_for("personal.pers_dashboard", guild=guild))

            property.property_owner_id = user.user_id
            db.session.commit()

            flash(f"Successfully transferred property.", "success")
            return redirect(url_for("personal.pers_dashboard", guild=guild))

    return render_template(
        "civ_dashboard.html",
        user=user if user is not None else None,
        logged_in=session.get("logged_in"),
        main_account=main_account,
        properties=properties,
        accounts=accounts,
        networth=networth,
        server=server,
        transactions=TransactionLog.query.filter_by(user_id=user.id),
        users=User.query.filter_by(user_associated_guild=guild),
    )


@personal.route(
    "/properties-dashboard", defaults={"guild": None}, methods=["GET", "POST"]
)
@personal.route("/properties-dashboard/<guild>", methods=["GET", "POST"])
def prop_dashboard(guild):
    user = None
    if not session.get("logged_in"):
        return redirect(url_for("login.index"))
    if not session.get("userid"):
        return redirect(url_for("login.index"))

    if not guild:
        return render_template(
            "choose_guild.html",
            user=user if user is not None else None,
            guilds=session.get("guilds"),
            logged_in=session.get("logged_in"),
        )

    user_exists = User.query.filter_by(
        user_id=session["userid"], user_associated_guild=guild
    ).first()
    if user_exists:
        user = user_exists
        user.user_email = session.get("email")
        db.session.commit()
    else:
        inserting_account = Account(
            account_user_id=session.get("userid"), account_guild_id=guild
        )
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(
            user_id=session.get("userid"),
            user_email=session.get("email"),
            user_name=session.get("name"),
            user_associated_guild=guild,
            user_main_account=inserting_account.id,
        )
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    properties = Property.query.filter_by(
        property_guild=guild, property_owner_id=None
    ).all()
    server = Server.query.filter_by(guild_id=guild).first()

    return render_template(
        "civ_properties.html",
        user=user if user is not None else None,
        logged_in=session.get("logged_in"),
        properties=properties,
        users=User.query.filter_by(user_associated_guild=guild),
        server=server,
    )
