# external imports
import os
import random
import traceback
from datetime import datetime, timedelta
from functools import wraps

import dash_core_components as dcc
import dash_html_components as html
#import shortuuid
import sqlalchemy
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from mailjet_rest import Client
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.sql import and_, select
from werkzeug.security import generate_password_hash

# local imports
from utilities.keys import FROM_EMAIL, MAILJET_API_KEY, MAILJET_API_SECRET

Column = sqlalchemy.Column
String = sqlalchemy.String
Integer = sqlalchemy.Integer
DateTime = sqlalchemy.DateTime
db = SQLAlchemy()
Column, String, Integer, DateTime = db.Column, db.String, db.Integer, db.DateTime





class User(db.Model):
    id = Column(Integer, primary_key=True)
    first = Column(String(100))
    last = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    role = Column(String(30), default="client")
    case = db.relationship('Case', backref='user', uselist=False )

def user_table():
    return Table("user", User.metadata)

case_currency = db.Table('case_currency',
   Column('case_id', Integer, db.ForeignKey('case.id')),
   Column('currency_id', Integer, db.ForeignKey('currency.id'))
)

class Case(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    user_id = Column(Integer, db.ForeignKey('user.id'))
    currencies = db.relationship('Currency', secondary=case_currency, back_populates='cases')

def case_table():
    return Table('case', Case.metadata)




class Currency(db.Model):
   id = Column(Integer,  primary_key=True)
   name = Column(String(30), nullable=False)
   cases = db.relationship('Case', secondary=case_currency, back_populates="currencies")

def currency_table():
    return Table('currency', Currency.metadata)



def add_user(first, last, password, email, engine, role=None):
    table = user_table()
    hashed_password = generate_password_hash(password, method="sha256")
    
    if role:
        values = dict(first=first, last=last, email=email, password=hashed_password, role=role)
    else:
        values = dict(first=first, last=last, email=email, password=hashed_password) 
    statement = table.insert().values(**values)
    #forRole = select([table.c.id]))
   
    conn = engine.connect()
    try:
        result = conn.execute(statement)
        
        #rs = conn.execute(forRole)
    except Exception as e:
        print(e)
    else:
        new_id = result.inserted_primary_key[0]
        #print(new_id)
        add_case('your_case', new_id, engine)
        conn.close()
        return print("User_case_added")
        

def show_users(engine):
    table = user_table()
    statement = select([table.c.first, table.c.last, table.c.email])

    conn = engine.connect()
    try:
        rs = conn.execute(statement)
    except Exception as e:
        print(e)
    else:
        one_user, all_users_dict = {}, []
        for row in rs:
            for column, value in row.items():
                one_user = {**one_user, **{column:value}}
            all_users_dict.append(one_user)
        #print(all_users_dict)

        conn.close()
        return all_users_dict

def del_user(email, engine):
    table = user_table()

    delete = table.delete().where(table.c.email == email)

    conn = engine.connect()
    conn.execute(delete)
    conn.close()

def user_exists(email, engine):
    """
    checks if the user exists with email <email>
    returns
        True if user exists
        False if user exists
    """
    table = user_table()
    statement = table.select().where(table.c.email == email)
    with engine.connect() as conn:
        resp = conn.execute(statement)
        ret = next(filter(lambda x: x.email == email, resp), False)
    return bool(ret)


def add_case(name, user_id, engine):
    table = case_table()

    values = dict(name=name, user_id=user_id)
    statement = table.insert().values(**values)

    conn = engine.connect()
    try: 
        conn.execute(statement)
    except Exception as e:
        print(e)
    else: 
        conn.close()
        return print("Case added")

def add_currency(name, engine):
    table = currency_table()

    values = dict(name=name)
    statement = table.insert().values(**values)

    conn = engine.connect()
    try: 
        conn.execute(statement)
    except Exception as e:
        print(e)
    else: 
        conn.close()
        return print("Currency added")


def add_currencyTo??ase(case_id, currency_id, engine):
    table = case_currency

    values = dict(case_id=case_id, currency_id=currency_id)
    statement = table.insert().values(**values)

    conn = engine.connect()
    try: 
        conn.execute(statement)
    except Exception as e:
        print(e)
    else: 
        conn.close()
        return print("Case and currency added")

def currency_exists_in_case(case_id, currency_id, engine):
    table = case_currency

    statement = table.select().where((table.c.case_id == case_id) and (table.c.currency_id == currency_id))
    conn = engine.connect()
    try:
        resp = conn.execute(statement)
        ret = next(filter(lambda x: x.case_id == case_id and x.currency_id == currency_id, resp), False)
    except Exception as e:
        print(e)
    else: 
        conn.close()
    return bool(ret)


def del_currency(name, engine):
    table = currency_table()

    delete = table.delete().where(table.c.name == name)

    conn = engine.connect()
    try:
        conn.execute(delete)
    except Exception as e:
        print(e)
    else:
        conn.close()
        return print('delete_currency')



def change_password(email, password, engine):
    if not user_exists(email, engine):
        return False

    table = user_table()
    hashed_password = generate_password_hash(password, method="sha256")
    values = dict(password=hashed_password)
    statement = table.update(table).where(table.c.email == email).values(values)

    with engine.connect() as conn:
        conn.execute(statement)

    # success value
    return True

def change_user(first, last, email, engine):
    # if there is no user in the database with that email, return False
    if not user_exists(email, engine):
        return False

    # otherwise, that user exists; update that user's info
    table = user_table()
    values = dict(first=first, last=last,)
    statement = table.update(table).where(table.c.email == email).values(values)
    with engine.connect() as conn:
        conn.execute(statement)
    # success value
    return True



class PasswordChange(db.Model):
    __tablename__ = "password_change"
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    password_key = Column(String(6))
    timestamp = Column(DateTime())


def password_change_table():
    return Table("password_change", PasswordChange.metadata)


def send_password_key(email, firstname, engine):
    """
    ensure email exists
    create random 6-number password key
    send email with Twilio Sendgrid containing that password key
    return True if that all worked
    return False if one step fails
    """

    # make sure email exists
    if not user_exists(email, engine):
        return False

    # generate password key
    key = "".join([random.choice("1234567890") for x in range(6)])

    table = user_table()
    statement = select([table.c.first]).where(table.c.email == email)
    with engine.connect() as conn:
        resp = list(conn.execute(statement))
        if len(resp) == 0:
            return False
        else:
            first = resp[0].first

    # send password key via email
    try:
        mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": {"Email": FROM_EMAIL, "Name": "My App"},
                    "To": [{"Email": email, "Name": first,}],
                    "Subject": "Greetings from Mailjet.",
                    "TextPart": "My App password reset code",
                    "HTMLPart": "<p>Dear {},<p> <p>Your My App password reset code is: <strong>{}</strong>".format(
                        firstname, key
                    ),
                    "CustomID": "AppGettingStartedTest",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result.status_code != "200":
            print("status not 200")
    except Exception as e:
        traceback.print_exc(e)
        return False

    # store that key in the password_key table
    table = password_change_table()
    values = dict(email=email, password_key=key, timestamp=datetime.now())
    statement = table.insert().values(**values)
    try:
        with engine.connect() as conn:
            conn.execute(statement)
    except:
        return False

    # change their current password to a random string
    # first, get first and last name
    random_password = "".join([random.choice("1234567890") for x in range(15)])
    res = change_password(email, random_password, engine)
    if res:
        # finished successfully
        return True
    return False


def validate_password_key(email, key, engine):
    # email exists
    if not user_exists(email, engine):
        return False

    # there is entry matching key and email
    table = password_change_table()
    statement = select([table.c.email, table.c.password_key, table.c.timestamp]).where(
        and_(table.c.email == email, table.c.password_key == key)
    )
    with engine.connect() as conn:
        resp = list(conn.execute(statement))
        if len(resp) == 1:
            if (resp[0].timestamp - (datetime.now() - timedelta(1))).days < 1:
                return True
        return False

    # finished with no erros; return True
    return True
