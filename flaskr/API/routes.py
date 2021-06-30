from flask import request, jsonify

from . import api
from .. import db
from ..models import Server, User, Property

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


@api.route('/api/v1.0/property/get_property_name', methods=['GET'])
def get_property_name():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    id = request.form.get('id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(property_guild=guild_id, property_name=name).first()

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

        return_json = {'response': 200, 'property_name': property.property_name}
        return jsonify(return_json)
    else:
        return_json = {'response': 401}
        return jsonify(return_json)


@api.route('/api/v1.0/property/get_property_name', methods=['GET'])
def get_property_name():
    key = request.form.get('api_key')
    guild_id = request.form.get('guild_id')
    name = request.form.get('guild_id')

    if key == "mJH^ZZzmrKm%TpvN95n27hvb4kjnQ5HP":
        property = Property.query.filter_by(property_guild=guild_id, property_name=name).first()

        return_json = {'response': 200, 'property_name': property.property_name}
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
