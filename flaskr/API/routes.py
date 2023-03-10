# ECOPLAY
# An economy system which connects discord and a website to enable roleplay communities and other fun communities to have an economic system.

# Copyright (C) 2022, Harry Smith.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
# You may contact me via hazzakak@gmail.com

import datetime
import time

from flask import request, jsonify

from . import api
from .. import db
from ..models import Server, TransactionLog, User, Property, Task, Account, AdminLog

""" example
@api.route('/api/v1.0/server/create_server', methods=['GET'])
def create_server():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "":
        return
    else:
        return_json = {'response': 401}
        return jsonify(return_json)
"""

"""
    Start of SERVER API
    - Create Server
    - Get/Set Starting Amount
    - Get/Set Banker Role
    - Get/Set Max Accounts
    - Get/Create Property
    - Get Users Properties
    - Get All Properties
    - Get All Unowned Properties
    
    -Get/Create User
    -Get/Create Account
    -Force Delete Account
"""


def add_transaction(userid, guildid, description):
    transaction = TransactionLog(
        user_id=userid, guild_id=guildid, description=description
    )
    db.session.add(transaction)
    db.session.commit()


def add_log(log):
    log = AdminLog(log=log)
    db.session.add(log)
    db.session.commit()


@api.route("/api/v1.0/server/create_server", methods=["GET"])
def create_server():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == "":
        new_server = Server(guild_id=guild_id)
        db.session.add(new_server)
        db.session.commit()

        add_log(f"Joined and created server: {new_server.id}")

        return_json = {"response": 200, "id": new_server.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/get_starting_amount", methods=["GET"])
def get_starting_amount():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == "":
        server = Server.query.filter_by(guild_id=guild_id).first()

        return_json = {"response": 200, "starting_amount": server.starting_amount}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/get_currency", methods=["GET"])
def get_currency():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == "":
        server = Server.query.filter_by(guild_id=guild_id).first()

        return_json = {"response": 200, "currency": server.currency}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/get_banker_role", methods=["GET"])
def get_banker_role():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == "":
        server = Server.query.filter_by(guild_id=int(guild_id)).first()

        try:
            return_json = {"response": 200, "banker_role": server.banker_role}
            return jsonify(return_json)
        except:
            return_json = {"response": 401}
            return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/get_max_accounts", methods=["GET"])
def get_max_accounts():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == "":
        server = Server.query.filter_by(guild_id=guild_id).first()

        return_json = {"response": 200, "max_accounts": server.max_accounts}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/set_starting_amount", methods=["GET"])
def set_starting_amount():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    new_value = request.form.get("new_value")
    person = request.form.get("person")

    if key == " ":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.starting_amount = new_value
        db.session.commit()

        add_log(f"Guild: {guild_id}. {person} set starting amount to: {new_value}")

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/set_currency", methods=["GET"])
def set_currency():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    new_value = request.form.get("new_value")
    person = request.form.get("person")

    if key == " ":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.currency = new_value
        db.session.commit()

        add_log(f"Guild: {guild_id}. {person} set currency to: {new_value}")

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/set_banker_role", methods=["GET"])
def set_banker_role():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    new_value = request.form.get("new_value")

    person = request.form.get("person")

    if key == " ":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.banker_role = new_value
        db.session.commit()

        add_log(f"Guild: {guild_id}. {person} set banking role to: {new_value}")

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/set_max_accounts", methods=["GET"])
def set_max_accounts():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    new_value = request.form.get("new_value")

    person = request.form.get("person")

    if key == " ":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.max_accounts = new_value
        db.session.commit()

        add_log(f"Guild: {guild_id}. {person} set max accounts to: {new_value}")

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/server/create_user", methods=["GET"])
def create_user():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")

    if key == " ":
        exists = User.query.filter_by(
            user_id=user_id, user_associated_guild=guild_id
        ).first()
        if exists:
            return_json = {"response": 200, "id": exists.id}
            return jsonify(return_json)

        server = Server.query.filter_by(guild_id=guild_id).first()
        new_account = Account(
            account_user_id=user_id,
            account_guild_id=guild_id,
            account_balance=server.starting_amount,
        )
        db.session.add(new_account)
        db.session.commit()

        new_user = User(
            user_associated_guild=guild_id,
            user_id=user_id,
            user_name=user_name,
            user_main_account=new_account.id,
        )
        db.session.add(new_user)
        db.session.commit()

        return_json = {"response": 200, "id": new_user.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


"""
    END OF SERVER API
"""

"""
    Start of PROPERTY API
    - Get Users Properties
    - Get All Properties
    - Get All Unowned Properties
    - Get/Set Property Name
    - Get/Set Property Value
    - Get/Set Property Owner
    - Delete Property
"""


@api.route("/api/v1.0/property/create_property", methods=["GET"])
def create_property():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    name = request.form.get("name")
    value = request.form.get("value")
    person = request.form.get("person")

    if key == " ":
        exists = Property.query.filter_by(property_name=name).first()
        if exists:
            return_json = {"response": 301}
            return jsonify(return_json)
        new_property = Property(
            property_name=name, property_value=value, property_guild=guild_id
        )
        db.session.add(new_property)
        db.session.commit()

        add_log(f"Guild: {guild_id}. {person} created property {name}.")

        return_json = {"response": 200, "id": new_property.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_users_properties", methods=["GET"])
def get_users_properties():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    user_id = request.form.get("user_id")

    if key == " ":
        properties = Property.query.filter_by(
            property_owner_id=user_id, property_guild=guild_id
        )

        rtn_lst = []
        for x in properties:
            rtn_lst.append(
                [
                    x.property_name,
                    x.property_value,
                    x.property_owner_id,
                    x.property_guild,
                ]
            )

        return_json = {"response": 200, "properties": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_all_properties", methods=["GET"])
def get_all_properties():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == " ":
        properties = Property.query.filter_by(property_guild=guild_id)

        rtn_lst = []
        for x in properties:
            rtn_lst.append(
                [
                    x.property_name,
                    x.property_value,
                    x.property_owner_id,
                    x.property_guild,
                ]
            )

        return_json = {"response": 200, "properties": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_all_unowned_properties", methods=["GET"])
def get_all_unowned_properties():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == " ":
        properties = Property.query.filter_by(
            property_guild=guild_id, property_owner_id=None
        )

        rtn_lst = []
        for x in properties:
            rtn_lst.append(
                [
                    x.property_name,
                    x.property_value,
                    x.property_owner_id,
                    x.property_guild,
                ]
            )

        return_json = {"response": 200, "properties": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_property_name", methods=["GET"])
def get_property_name():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    id = request.form.get("id")

    if key == " ":
        property = Property.query.filter_by(property_guild=guild_id, id=id).first()

        if not property:
            return_json = {"response": 302}
            return jsonify(return_json)

        return_json = {"response": 200, "property_name": property.property_name}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_property_value", methods=["GET"])
def get_property_value():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    name = request.form.get("name")

    if key == " ":
        property = Property.query.filter_by(
            property_guild=guild_id, property_name=name
        ).first()

        if not property:
            return_json = {"response": 302}
            return jsonify(return_json)

        return_json = {
            "response": 200,
            "id": property.id,
            "property_value": property.property_value,
        }
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_property_owner", methods=["GET"])
def get_property_owner():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    name = request.form.get("name")

    if key == " ":
        property = Property.query.filter_by(
            property_guild=guild_id, property_name=name
        ).first()

        return_json = {
            "response": 200,
            "id": property.id,
            "property_owner": property.property_owner_id,
        }
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/get_property_exists", methods=["GET"])
def get_property_exists():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    name = request.form.get("name")

    if key == " ":
        property = Property.query.filter_by(
            property_guild=guild_id, property_name=name
        ).first()

        return_json = {"response": 200, "exists": True if property else False}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/set_property_name", methods=["GET"])
def set_property_name():
    key = request.form.get("api_key")
    id = request.form.get("id")
    new_value = request.form.get("new_value")

    if key == " ":
        property = Property.query.filter_by(id=id).first()
        property.property_name = new_value
        db.session.commit()

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/set_property_value", methods=["GET"])
def set_property_value():
    key = request.form.get("api_key")
    name = request.form.get("name")
    guild = request.form.get("guild")
    new_value = request.form.get("new_value")
    person = request.form.get("person")

    if key == " ":
        property = Property.query.filter_by(
            property_name=name, property_guild=guild
        ).first()
        property.property_value = new_value
        db.session.commit()

        add_log(f"Guild: {guild}. {person} set property value of {name}.")

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/set_property_owner", methods=["GET"])
def set_property_owner():
    key = request.form.get("api_key")
    name = request.form.get("name")
    guild = request.form.get("guild")
    new_value = request.form.get("new_value")
    person = request.form.get("person")

    if key == " ":
        property = Property.query.filter_by(
            property_name=name, property_guild=guild
        ).first()
        property.property_owner_id = new_value
        db.session.commit()

        add_log(f"Guild: {guild}. {person} set property owner of {name}.")
        add_transaction(new_value, guild, f"Received property {property.property_name}")

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/property/delete_property", methods=["GET"])
def delete_property():
    key = request.form.get("api_key")
    guild = request.form.get("guild")
    name = request.form.get("name")

    if key == " ":
        property = Property.query.filter_by(
            property_guild=guild, property_name=name
        ).first()
        db.session.delete(property)
        db.session.commit()

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


"""
    END OF PROPERTY API
"""

"""
    Start of TASK API
    - Get/Create Tasks
    - Get/Set Task Type
    - Get/Set Task Target ID
    - Get/Set Task Guild ID
    - Get/Set Task Amount
    - Get/Set Task Frequency
    - Get/Set Next Due
"""


@api.route("/api/v1.0/task/get_tasks", methods=["GET"])
def get_tasks():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")

    if key == " ":
        tasks = Task.query.filter_by(guild_id=guild_id)

        rtn_lst = []
        for x in tasks:
            rtn_lst.append(
                [
                    x.id,
                    x.type,
                    x.target_id,
                    x.guild_id,
                    x.amount,
                    x.frequency,
                    x.next_due,
                ]
            )

        return_json = {"response": 200, "tasks": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/get_all_tasks_today", methods=["GET"])
def get_all_tasks_today():
    key = request.form.get("api_key")

    print(key)

    if key == " " or key == None:
        tasks = Task.query.filter(
            Task.next_due <= datetime.datetime.today().date()
        ).all()

        rtn_lst = []
        for x in tasks:
            rtn_lst.append(
                [
                    x.id,
                    x.type,
                    x.target_id,
                    x.guild_id,
                    x.amount,
                    x.frequency,
                    x.next_due,
                ]
            )

        return_json = {"response": 200, "tasks": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/get_task", methods=["GET"])
def get_task():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        task = Task.query.filter_by(id=id).first()

        rtn_lst = [
            task.id,
            task.type,
            task.target_id,
            task.guild_id,
            task.amount,
            task.frequency,
            task.next_due,
        ]

        return_json = {"response": 200, "task": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/get_task_type", methods=["GET"])
def get_task_type():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        task = Task.query.filter_by(id=id).first()

        return_json = {"response": 200, "type": task.type}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/get_task_target_id", methods=["GET"])
def get_task_target_id():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        task = Task.query.filter_by(id=id).first()

        return_json = {"response": 200, "target_id": task.target_id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/set_next_due", methods=["GET"])
def set_next_due():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        task = Task.query.filter_by(id=id).first()
        frequency = task.frequency * 24 * 60 * 60
        now = time.time()
        next_due = int(now) + int(frequency)
        dt_object = datetime.datetime.fromtimestamp(next_due)

        task.next_due = dt_object.date()
        db.session.commit()

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/get_task_frequency", methods=["GET"])
def get_task_frequency():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        task = Task.query.filter_by(id=id).first()

        return_json = {"response": 200, "frequency": task.frequency}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/task/create_task", methods=["GET"])
def create_task():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    task_type = request.form.get("task_type")
    target_id = request.form.get("target_id")
    amount = request.form.get("amount")
    frequency = request.form.get("frequency")

    if key == " ":
        new_task = Task(
            guild_id=guild_id,
            type=task_type,
            target_id=target_id,
            amount=amount,
            frequency=frequency,
        )
        db.session.add(new_task)
        db.session.commit()

        return_json = {"response": 200, "id": new_task.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


"""
    END OF TASK API
"""

"""
    Start of ACCOUNT API
    - Get/Create Tasks
    - Get/Set Task Type
    - Get/Set Task Target ID
    - Get/Set Task Guild ID
    - Get/Set Task Amount
    - Get/Set Task Frequency
    - Get/Set Next Due
"""


@api.route("/api/v1.0/account/create_account", methods=["GET"])
def create_account():
    key = request.form.get("api_key")
    guild_id = request.form.get("guild_id")
    user_id = request.form.get("user_id")
    new = request.form.get("new")
    name = request.form.get("name")

    server = Server.query.filter_by(guild_id=guild_id).first()
    accounts = Account.query.filter_by(
        account_user_id=user_id, account_guild_id=guild_id
    )

    if key == " ":
        if accounts.count() == server.max_accounts:
            return_json = {"response": 400}
            return jsonify(return_json)

        new_account = Account(
            account_user_id=user_id,
            account_guild_id=guild_id,
            account_name=name,
            account_balance=server.starting_amount if eval(new) else 0,
        )
        db.session.add(new_account)
        db.session.commit()

        add_transaction(
            new_account.account_user.account_user_id,
            guild_id,
            f"Created new account {new_account.id}",
        )

        return_json = {"response": 200, "id": new_account.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/get_account", methods=["GET"])
def get_account():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        account = Account.query.filter_by(id=id).first()

        rtn_lst = [
            account.id,
            account.account_user_id,
            account.account_guild_id,
            account.account_name,
            account.account_balance,
        ]

        return_json = {"response": 200, "account": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/get_default_account", methods=["GET"])
def get_default_account():
    key = request.form.get("api_key")
    user_id = request.form.get("user_id")
    guild_id = request.form.get("guild_id")

    if key == " ":
        user = User.query.filter_by(
            user_id=user_id, user_associated_guild=guild_id
        ).first()
        if user is None:
            new_user = User(user_id=user_id, user_associated_guild=guild_id)
            new_account = Account(account_user_id=user_id, account_guild_id=guild_id)
            db.session.add(new_user)
            db.session.add(new_account)
            db.session.commit()

            account = Account.query.filter_by(id=new_account.id).first()
        else:
            account = Account.query.filter_by(id=user.user_main_account).first()

        rtn_lst = [
            account.id,
            account.account_user_id,
            account.account_guild_id,
            account.account_name,
            account.account_balance,
        ]

        return_json = {"response": 200, "account": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/set_default_account", methods=["GET"])
def set_default_account():
    key = request.form.get("api_key")
    id = request.form.get("id")
    user_id = request.form.get("user_id")
    guild = request.form.get("guild_id")

    if key == " ":
        user = User.query.filter_by(
            user_id=user_id, user_associated_guild=guild
        ).first()
        user.user_main_account = id
        db.session.commit()

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/get_accounts", methods=["GET"])
def get_accounts():
    key = request.form.get("api_key")
    user_id = request.form.get("user_id")
    guild_id = request.form.get("guild_id")

    if key == " ":
        accounts = Account.query.filter_by(
            account_user_id=user_id, account_guild_id=guild_id
        )

        rtn_lst = []
        for x in accounts:
            rtn_lst.append(
                [
                    x.id,
                    x.account_user_id,
                    x.account_guild_id,
                    x.account_name,
                    x.account_balance,
                ]
            )

        return_json = {"response": 200, "accounts": rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/delete_account", methods=["GET"])
def delete_account():
    key = request.form.get("api_key")
    id = request.form.get("id")
    account = Account.query.filter_by(id=id).first()

    if key == " ":
        accounts = Account.query.filter_by(
            account_user_id=account.account_user_id,
            account_guild_id=account.account_guild_id,
        )
        if accounts.count() == 1:
            return_json = {"response": 400}
            return jsonify(return_json)

        db.session.delete(account)
        db.session.commit()

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/get_account_name", methods=["GET"])
def get_account_name():
    key = request.form.get("api_key")
    id = request.form.get("id")

    if key == " ":
        account = Account.query.filter_by(id=id).first()

        return_json = {"response": 200, "account_name": account.account_name}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/set_account_name", methods=["GET"])
def set_account_name():
    key = request.form.get("api_key")
    id = request.form.get("id")
    name = request.form.get("name")

    if key == " ":
        account = Account.query.filter_by(id=id).first()
        account.account_name = name
        db.session.commit()

        return_json = {"response": 200}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/deposit", methods=["GET"])
def deposit():
    key = request.form.get("api_key")
    id = request.form.get("id")
    amount = request.form.get("amount")

    if key == " ":
        account = Account.query.filter_by(id=id).first()
        account.account_balance += int(amount)
        db.session.commit()

        add_transaction(
            account.account_user_id,
            account.account_guild_id,
            f"{amount} was deposited into your account: {id}",
        )

        return_json = {"response": 200, "account_id": account.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)


@api.route("/api/v1.0/account/withdraw", methods=["GET"])
def withdraw():
    key = request.form.get("api_key")
    id = request.form.get("id")
    amount = request.form.get("amount")
    cannot_negative = request.form.get("amount") if "amount" in request.form else False

    if key == " ":
        account = Account.query.filter_by(id=id).first()
        if cannot_negative and account.account_balance - int(amount) < 0:
            return_json = {"response": 400}
            return jsonify(return_json)

        account.account_balance -= int(amount)
        db.session.commit()

        add_transaction(
            account.account_user_id,
            account.account_guild_id,
            f"{amount} was withdrawn from your account: {id}",
        )

        return_json = {"response": 200, "account_id": account.id}
        return jsonify(return_json)
    else:
        return_json = {"response": 401}
        return jsonify(return_json)
