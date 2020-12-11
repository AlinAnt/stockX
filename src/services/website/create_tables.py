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
    user_exists,
    add_case,
    add_currency,
    add_currencyToСase
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
try:
    create_user_table(User,engine)
    create_password_change_table(PasswordChange,engine)
    create_case_table(Case,engine)
    create_currency_table(Currency,engine)
    print("Tables created")
except Exception as e:
    print("Error occurred during Table creation!")
    print(e)


#add a test user to the database
#first = 'Nika'
#last = 'Redy'
#email = 'Nika@test.com'
#password = '12345'

#add_user(first,last,password,email, engine)
#name = "Ret"
#user_id = 3
#add_case(name, user_id, engine)
#сurr_name = "Bitcoin"
#add_currency(curr_name, engine)
#name = "XRP"
#add_currency(name, engine)
# show that the users exists
#show_users(engine)
#case_id = 1
#currency_id = 1
#add_currencyToСase(case_id, currency_id, engine)
# confirm that user exists
#print(user_exists(email,engine))



