from flask import render_template, session, url_for, request, flash
from werkzeug.utils import redirect

from . import personal
from .. import db
from ..models import User, Account, Property, Server, TransactionLog

API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '767749360586326026'
CLIENT_SECRET = 'B8JBIE949Ak5DZZ-6DsmD4mG20Rf1U_S'
REDIRECT_URI = 'http://localhost:5000/discord/auth'


@personal.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    code = request.args.get('account_id')
    account = Account.query.filter_by(id=int(code)).first()
    if int(account.account_user_id) != int(session['userid']):
        flash('Naughty! This is not your account to delete! *tuts* ', 'danger')
        return redirect(url_for("personal.pers_dashboard"))

    user = User.query.filter_by(user_id=session['userid'], user_associated_guild=account.account_guild_id).first()
    main_account = Account.query.filter_by(id=user.user_main_account).first()

    if account.id == main_account.id:
        flash('You sadly cannot delete your debts away, you need to keep your main account.', 'danger')
        return redirect(url_for("personal.pers_dashboard", guild=account.account_guild_id))

    main_account.account_balance += account.account_balance
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for("personal.pers_dashboard", guild=account.account_guild_id))


@personal.route('/personal-dashboard', defaults={'guild': None}, methods=['GET', 'POST'])
@personal.route('/personal-dashboard/<guild>', methods=['GET', 'POST'])
def pers_dashboard(guild):
    user = None
    if not session['logged_in']:
        return redirect(url_for("login.index"))
    if not session['userid']:
        return redirect(url_for("login.index"))

    if not guild:
        return render_template('choose_guild.html', user=user if user is not None else None, guilds=session['guilds'],
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

    main_account = Account.query.filter_by(id=user.user_main_account).first()
    properties = Property.query.filter_by(property_guild=guild, property_owner_id=user.id).all()
    accounts = Account.query.filter_by(account_user_id=session['userid'], account_guild_id=guild)
    server = Server.query.filter_by(guild_id=guild).first()
    networth = 0

    for p in properties:
        networth += p.property_value

    for a in accounts:
        networth += a.account_balance

    if request.method == 'POST':
        account_name = request.form.get('account_name')
        inserting_account = Account(account_user_id=session['userid'], account_guild_id=guild,
                                    account_name=account_name, account_balance=0)
        db.session.add(inserting_account)
        db.session.commit()

    return render_template('civ_dashboard.html', user=user if user is not None else None,
                           logged_in=session['logged_in'], main_account=main_account, properties=properties,
                           accounts=accounts, networth=networth, server=server,
                           transactions=TransactionLog.query.filter_by(user_id=user.id))
