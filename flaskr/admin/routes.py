from flask import render_template, session, url_for, flash, request
from werkzeug.utils import redirect

from . import admin
from .. import db
from ..models import User, Account, Server, Property, TransactionLog

API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_ID = '767749360586326026'
CLIENT_SECRET = 'B8JBIE949Ak5DZZ-6DsmD4mG20Rf1U_S'
REDIRECT_URI = 'http://localhost:5000/discord/auth'


@admin.route('/delete_property', methods=['GET', 'POST'])
def delete_account():
    code = request.args.get('property_id')
    property = Property.query.filter_by(id=int(code)).first()
    isAdmin = False

    for g in session['guilds']:
        if g[2] and int(property.property_guild) == int(g[1]):
            isAdmin = True
            break
        else:
            continue

    if not isAdmin:
        flash('Naughty! You are not allowed to delete this property! *tuts* ', 'danger')
        return redirect(url_for("admin.admin_dashboard"))

    db.session.delete(property)
    db.session.commit()
    return redirect(url_for("admin.properties_dashboard", guild=property.property_guild))


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

    if request.method == 'POST':
        if 'edit_property_name' in request.form:
            property_id = request.form.get('edit_property_id')
            property_name = request.form.get('edit_property_name')
            property_value = request.form.get('edit_property_value')
            property_owner = request.form.get('edit_property_owner')

            property = Property.query.filter_by(id=property_id).first()

            property.property_name = property_name
            property.property_value = property_value
            property.property_owner_id = int(property_owner)

            db.session.commit()
            flash('You have edited the property.', 'success')
            return redirect(url_for("admin.properties_dashboard", guild=guild))

        if 'property_name' in request.form:
            property_name = request.form.get('property_name')
            property_value = request.form.get('property_value')
            property_owner = request.form.get('property_owner')

            property_exists = Property.query.filter_by(property_name=property_name).first()
            if property_exists:
                flash("A property already exists with this name.", 'danger')
                return redirect(url_for("admin.properties_dashboard", guild=guild))

            property_user = User.query.filter_by(user_id=property_owner).first()

            new_property = Property(property_name=property_name, property_value=property_value,
                                    property_owner_id=property_user.user_id if property_user else None, property_guild=guild)
            db.session.add(new_property)
            db.session.commit()

            trans = TransactionLog(user_id=new_property.property_owner_id,
                                   description=f"Property transferred. Value: {server.currency}{new_property.property_value}")
            db.session.add(trans)
            db.session.commit()

            flash('You have created a property.', 'success')

    return render_template('admin_properties.html', user=user if user is not None else None,
                           logged_in=session['logged_in'], server=server, properties=properties,
                           users=User.query.filter_by(user_associated_guild=guild))
