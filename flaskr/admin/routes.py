from flask import render_template, session, url_for, flash, request
from werkzeug.utils import redirect

from . import admin
from .. import db
from ..models import User, Account, Server, Property

API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '767749360586326026'
CLIENT_SECRET = 'B8JBIE949Ak5DZZ-6DsmD4mG20Rf1U_S'
REDIRECT_URI = 'http://localhost:5000/discord/auth'


@admin.route('/admin-dashboard', defaults={'guild': None}, methods=['GET', 'POST'])
@admin.route('/admin-dashboard/<guild>', methods=['GET', 'POST'])
def admin_dashboard(guild):
    user = None
    if not session['logged_in']:
        return redirect(url_for("login.index"))
    if not session['userid']:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template('choose_guild.html', user=user if user is not None else None, guilds=session['guilds'],
                               logged_in=session['logged_in'])

    isAdmin = False

    for g in session['guilds']:
        if g[2] and int(guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("You're not an admin in this server.", 'danger')
        return render_template('choose_guild.html', user=user if user is not None else None,
                               guilds=session['guilds'],
                               logged_in=session['logged_in'])

    user_exists = User.query.filter_by(user_id=session['userid'], user_associated_guild=guild).first()
    if user_exists:
        user = user_exists
    else:
        inserting_account = Account(account_user_id=session['userid'], account_guild_id=guild)
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(user_id=session['userid'], user_email=session['email'], user_name=session['name'],
                              user_associated_guild=guild, user_main_account=inserting_account.id)
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    server = Server.query.filter_by(guild_id=guild).first()

    if request.method == 'POST':
        max_accounts = request.form.get('max_accounts')
        banker_role = request.form.get('banker_role')
        currency = request.form.get('currency')
        starting_amount = request.form.get('starting_amount')

        server.max_accounts = max_accounts
        server.banker_role = banker_role
        server.currency = currency
        server.starting_amount = starting_amount
        db.session.commit()
        flash('You have updated the servers settings.', 'success')

    return render_template('admin_dashboard.html', user=user if user is not None else None,
                           logged_in=session['logged_in'], server=server)

@admin.route('/properties', defaults={'guild': None}, methods=['GET', 'POST'])
@admin.route('/properties/<guild>', methods=['GET', 'POST'])
def properties_dashboard(guild):
    user = None
    if not session['logged_in']:
        return redirect(url_for("login.index"))
    if not session['userid']:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template('choose_guild.html', user=user if user is not None else None, guilds=session['guilds'],
                               logged_in=session['logged_in'])

    isAdmin = False

    for g in session['guilds']:
        if g[2] and int(guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash("You're not an admin in this server.", 'danger')
        return render_template('choose_guild.html', user=user if user is not None else None,
                               guilds=session['guilds'],
                               logged_in=session['logged_in'])

    user_exists = User.query.filter_by(user_id=session['userid'], user_associated_guild=guild).first()
    if user_exists:
        user = user_exists
    else:
        inserting_account = Account(account_user_id=session['userid'], account_guild_id=guild)
        db.session.add(inserting_account)
        db.session.commit()

        inserting_user = User(user_id=session['userid'], user_email=session['email'], user_name=session['name'],
                              user_associated_guild=guild, user_main_account=inserting_account.id)
        db.session.add(inserting_user)
        db.session.commit()

        user = inserting_user

    server = Server.query.filter_by(guild_id=guild).first()
    properties = Property.query.filter_by(property_guild=guild)

    for p in properties:
        print(p.property_owner.user_name)

    return render_template('admin_properties.html', user=user if user is not None else None,
                           logged_in=session['logged_in'], server=server, properties=properties)