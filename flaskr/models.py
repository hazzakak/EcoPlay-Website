import datetime

from sqlalchemy.orm import backref

from flaskr import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_associated_guild = db.Column(db.Integer)
    user_main_account = db.Column(db.Integer)
    user_accounts = db.Column(db.String)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def create_user(self, user_id):
        return


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_user_id = db.Column(db.Integer, nullable=False)
    account_guild_id = db.Column(db.Integer, nullable=False)
    account_name = db.Column(db.String(120), server_default='Main Account')
    account_balance = db.Column(db.Integer, server_default='0')

    def __repr__(self):
        return '<Account %r>' % self.id

    def __init__(self, account_name, account_balance):
        self.account_name = account_name
        self.account_balance = account_balance

    def delete_account(self):
        return

    def create_account(self):
        return

    def set_default_account(self):
        return

    @classmethod
    def deposit(cls, amount, **kw):
        obj = cls(**kw)
        obj.account_balance += amount
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def withdraw(cls, amount, **kw):
        obj = cls(**kw)
        obj.account_balance += amount
        db.session.add(obj)
        db.session.commit()


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.Integer, nullable=False)
    property_value = db.Column(db.Integer, server_default='0')
    property_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    property_owner = db.relationship('User', backref=backref('user', uselist=False))
    property_guild = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Property %r>' % self.property_name

    def update_name(self):
        return

    def update_value(self):
        return

    def update_owner(self):
        return


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.Integer, nullable=False, unique=True)
    max_accounts = db.Column(db.Integer, server_default='3')
    banker_role = db.Column(db.Integer)
    starting_amount = db.Column(db.Integer, server_default='1500')
    currency = db.Column(db.String(5), server_default='$')

    def __repr__(self):
        return '<Server %r>' % self.id

    def set_starting_amount(self):
        return

    def set_banker_role(self):
        return

    def set_max_accounts(self):
        return


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, server_default='person')
    target_id = db.Column(db.Integer)
    guild_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    next_due = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r>' % self.id


class TransactionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    description = db.Column(db.String)
    time = db.Column(db.String, server_default=str(datetime.datetime.utcnow()))

    def __repr__(self):
        return '<Transaction Log %r>' % self.id
