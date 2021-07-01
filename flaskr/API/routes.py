import datetime
import time

from flask import request, jsonify

from . import api
from .. import db
from ..models import Server, User, Property, Task, Account

''' example
@api.route('/api/v1.0/server/create_server', methods=['GET'])
def create_server():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        return
    else:
        return_json = {'response': 401}
        return jsonify(return_json)
'''

'''
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
'''


@api.route('/api/v1.0/server/create_server', methods=['GET'])
def create_server():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        new_server = Server(guild_id=guild_id)
        db.session.add(new_server)
        db.session.commit()

        return_json = {'response': 200, 'id': new_server.id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/get_starting_amount', methods=['GET'])
def get_starting_amount():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        server = Server.query.filter_by(guild_id=guild_id).first()

        return_json = {'response': 200, 'starting_amount': server.starting_amount}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/get_banker_role', methods=['GET'])
def get_banker_role():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        server = Server.query.filter_by(guild_id=guild_id).first()

        return_json = {'response': 200, 'banker_role': server.banker_role}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/get_max_accounts', methods=['GET'])
def get_max_accounts():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        server = Server.query.filter_by(guild_id=guild_id).first()

        return_json = {'response': 200, 'max_accounts': server.max_accounts}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/set_starting_amount', methods=['GET'])
def set_starting_amount():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    new_value = request.form.get('new_value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.starting_amount = new_value
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/set_banker_role', methods=['GET'])
def set_banker_role():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    new_value = request.form.get('new_value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.banker_role = new_value
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/set_max_accounts', methods=['GET'])
def set_max_accounts():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    new_value = request.form.get('new_value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        server = Server.query.filter_by(guild_id=guild_id).first()
        server.max_accounts = new_value
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/server/create_user', methods=['GET'])
def create_user():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    user_id = request.form.get('user_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        new_user = User(user_associated_guild=guild_id, user_id=user_id)
        db.session.add(new_user)
        db.session.commit()

        return_json = {'response': 200, 'id': new_user.id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


'''
    END OF SERVER API
'''

'''
    Start of PROPERTY API
    - Get Users Properties
    - Get All Properties
    - Get All Unowned Properties
    - Get/Set Property Name
    - Get/Set Property Value
    - Get/Set Property Owner
    - Delete Property
'''


@api.route('/api/v1.0/property/create_property', methods=['GET'])
def create_property():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    name = request.form.get('name')
    value = request.form.get('value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        new_property = Property(property_name=name, property_value=value, property_guild=guild_id)
        db.session.add(new_property)
        db.session.commit()

        return_json = {'response': 200, 'id': new_property.id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_users_properties', methods=['GET'])
def get_users_properties():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    user_id = request.form.get('user_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        properties = Property.query.filter_by(property_owner_id=user_id, property_guild=guild_id)

        rtn_lst = []
        for x in properties:
            rtn_lst.append([x.property_name, x.property_value, x.property_owner_id, x.property_guild])

        return_json = {'response': 200, 'properties': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_all_properties', methods=['GET'])
def get_all_properties():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        properties = Property.query.filter_by(property_guild=guild_id)

        rtn_lst = []
        for x in properties:
            rtn_lst.append([x.property_name, x.property_value, x.property_owner_id, x.property_guild])

        return_json = {'response': 200, 'properties': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_all_unowned_properties', methods=['GET'])
def get_all_unowned_properties():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        properties = Property.query.filter_by(property_guild=guild_id, property_owner_id=None)

        rtn_lst = []
        for x in properties:
            rtn_lst.append([x.property_name, x.property_value, x.property_owner_id, x.property_guild])

        return_json = {'response': 200, 'properties': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_property_name', methods=['GET'])
def get_property_name():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(property_guild=guild_id, id=id).first()

        if not property:
            return_json = {'response': 302}
            return jsonify(return_json)

        return_json = {'response': 200, 'property_name': property.property_name}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_property_value', methods=['GET'])
def get_property_value():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    name = request.form.get('name')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(property_guild=guild_id, property_name=name).first()

        if not property:
            return_json = {'response': 302}
            return jsonify(return_json)

        return_json = {'response': 200, 'id': property.id, 'property_name': property.property_name}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_property_owner', methods=['GET'])
def get_property_owner():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    name = request.form.get('name')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(property_guild=guild_id, property_name=name).first()

        return_json = {'response': 200, 'id': property.id, 'property_owner': property.property_owner_id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/set_property_name', methods=['GET'])
def set_starting_amount():
    key = request.form.get('api_key')
    id = request.form.get('id')
    new_value = request.form.get('new_value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(id=id).first()
        property.property_name = new_value
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/set_property_value', methods=['GET'])
def set_property_value():
    key = request.form.get('api_key')
    id = request.form.get('id')
    new_value = request.form.get('new_value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(id=id).first()
        property.property_value = new_value
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/set_property_owner', methods=['GET'])
def set_property_value():
    key = request.form.get('api_key')
    id = request.form.get('id')
    new_value = request.form.get('new_value')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(id=id).first()
        property.property_owner = new_value
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/delete_property', methods=['GET'])
def delete_property():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(id=id).first()
        db.session.delete(property)
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


'''
    END OF PROPERTY API
'''

'''
    Start of TASK API
    - Get/Create Tasks
    - Get/Set Task Type
    - Get/Set Task Target ID
    - Get/Set Task Guild ID
    - Get/Set Task Amount
    - Get/Set Task Frequency
    - Get/Set Next Due
'''


@api.route('/api/v1.0/task/get_tasks', methods=['GET'])
def get_tasks():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        tasks = Task.query.filter_by(guild_id=guild_id)

        rtn_lst = []
        for x in tasks:
            rtn_lst.append([x.id, x.type, x.target_id, x.guild_id, x.amount, x.frequency, x.next_due])

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/task/get_task', methods=['GET'])
def get_task():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        task = Task.query.filter_by(id=id).first()

        rtn_lst = [task.id, task.type, task.target_id, task.guild_id, task.amount, task.frequency, task.next_due]

        return_json = {'response': 200, 'task': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/task/get_task_type', methods=['GET'])
def get_task_type():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        task = Task.query.filter_by(id=id).first()

        return_json = {'response': 200, 'type': task.type}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/task/get_task_target_id', methods=['GET'])
def get_task_target_id():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        task = Task.query.filter_by(id=id).first()

        return_json = {'response': 200, 'target_id': task.target_id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/task/set_next_due', methods=['GET'])
def set_next_due():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        task = Task.query.filter_by(id=id).first()
        frequency = task.frequency * 24 * 60 * 60
        now = time.time()
        next_due = now + frequency
        dt_object = datetime.datetime.fromtimestamp(next_due)

        task.next_due = dt_object.date()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/task/get_task_frequency', methods=['GET'])
def get_task_frequency():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        task = Task.query.filter_by(id=id).first()

        return_json = {'response': 200, 'frequency': task.frequency}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/task/create_task', methods=['GET'])
def create_task():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    task_type = request.form.get('task_type')
    target_id = request.form.get('target_id')
    amount = request.form.get('amount')
    frequency = request.form.get('frequency')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        new_task = Task(guild_id=guild_id, type=task_type, target_id=target_id, amount=amount, frequency=frequency)
        db.session.add(new_task)
        db.session.commit()

        return_json = {'response': 200, 'id': new_task.id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


'''
    END OF TASK API
'''

'''
    Start of ACCOUNT API
    - Get/Create Tasks
    - Get/Set Task Type
    - Get/Set Task Target ID
    - Get/Set Task Guild ID
    - Get/Set Task Amount
    - Get/Set Task Frequency
    - Get/Set Next Due
'''


@api.route('/api/v1.0/account/create_account', methods=['GET'])
def create_account():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    user_id = request.form.get('user_id')
    new = request.form.get('new') if 'new' in request.form else False
    name = request.form.get('name')

    server = Server.query.filter_by(guild_id=guild_id).first()
    accounts = Account.query.filter_by(account_user_id=user_id, account_guild=guild_id)

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        if len(accounts) == server.max_accounts:
            return_json = {'response': 400}
            return jsonify(return_json)

        new_account = Account(account_user_id=user_id, account_guild_id=guild_id, account_name=name,
                              account_balance=server.starting_amount if new else 0)
        db.session.add(new_account)
        db.session.commit()

        return_json = {'response': 200, 'id': new_account.id}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/account/get_account', methods=['GET'])
def get_account():
    key = request.form.get('api_key')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        account = Account.query.filter_by(id=id).first()

        rtn_lst = [account.id, account.account_user_id, account.account_guild_id, account.account_name,
                   account.account_balance]

        return_json = {'response': 200, 'account': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/account/get_default_account', methods=['GET'])
def get_account():
    key = request.form.get('api_key')
    user_id = request.form.get('user_id')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        user = User.query.filter_by(user_id=user_id, user_associated_guild=guild_id).first()
        account = Account.query.filter_by(id=user.user_main_account).first()

        rtn_lst = [account.id, account.account_user_id, account.account_guild_id, account.account_name,
                   account.account_balance]

        return_json = {'response': 200, 'account': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/account/get_accounts', methods=['GET'])
def get_accounts():
    key = request.form.get('api_key')
    user_id = request.form.get('user_id')
    guild_id = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        accounts = Account.query.filter_by(account_user_id=user_id, account_guild_id=guild_id)

        rtn_lst = []
        for x in accounts:
            rtn_lst.append([x.id, x.account_user_id, x.account_guild_id, x.account_name,
                            x.account_balance])

        return_json = {'response': 200, 'accounts': rtn_lst}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/account/delete_account', methods=['GET'])
def delete_account():
    key = request.form.get('api_key')
    id = request.form.get('id')
    account = Account.query.filter_by(id=id).first()

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        accounts = Account.query.filter_by(account_user_id=account.account_user_id,
                                           account_guild=account.account_guild_id)
        if len(accounts) == 1:
            return_json = {'response': 400}
            return jsonify(return_json)

        db.session.delete(account)
        db.session.commit()

        return_json = {'response': 200}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)
