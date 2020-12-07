from utilities.config import engine
from utilities.auth import (
    User,
    PasswordChange,
    Case,
    Currency,
    case_currency,
    add_user,
    change_user,
    del_user,
    show_users,
    user_exists
)


# engine is open to sqlite///users.db

def create_user_table(model,engine):
    model.metadata.create_all(engine)

def create_password_change_table(model,engine):
    model.metadata.create_all(engine)

def create_case_table(model, engine):
    model.metadata.create_all(engine)

def create_currency_table(model, engine):
    model.metadata.create_all(engine)

# create the tables
create_user_table(User,engine)
create_password_change_table(PasswordChange,engine)
create_case_table(Case,engine)
create_currency_table(Currency,engine)
#case_currency.create(engine)

# add a test user to the database
#first = 'Sarna'
#last = 'rss'
#email = 'Rita@admin.com'
#password = '12345'
#add_user(first,last,password,email, engine)


# show that the users exists
show_users(engine)

# confirm that user exists
#print(user_exists(email,engine))


