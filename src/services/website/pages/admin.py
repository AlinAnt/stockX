import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
from flask_login import current_user
import time
from server import app, User
from utilities.config import engine
from utilities.auth import show_users, del_user

success_alert = dbc.Alert(
    'Logged in successfully. Taking you home!',
    color='success',
    dismissable=True
)

def layout():
    return html.Div([
        html.Div(id='admin-alert'),
        build_main_layout()
    ])
       
def generate_user_row(col1, col2, col3, col4, header=True):
    if header:
        return html.Tr(children=[
            html.Th(scope="col", children=col1),
            html.Th(scope="col", children=col2),
            html.Th(scope="col", children=col3),
            html.Th(scope="col", children=col4),
            #html.Th(scope="col", children=col5),
        ])
    else:
        return html.Tr(children=[
           html.Th(scope="col", children=col1),
           html.Td(children=col2),
           html.Td(children=col3),
           #html.Td(children=col4),
           html.Td(dbc.Button("Удалить", color='danger', id=col4)),
        ])

def generate_table():
    result = []
    users = show_users(engine)
    for idx, user in enumerate(users):
        #print(type(user))
        user_data = list(user.values())
        #print(type(user_data))
        name = user_data[0]
        surname = user_data[1]
        email = user_data[2]
      
       
        result.append(generate_user_row(
            name, surname, email, str(idx), False
        ))
    return html.Tbody(children=result)


def generate_user_list_header():
    return generate_user_row(
      'Имя', 'Фамилия', 'email', 'Хочешь удалить?'
    )

def build_main_layout():
    return html.Table(
        id='top-section-container',
        className="table",
        children=[
            html.Thead(
                children=[
                    generate_user_list_header()
                ],
            ),
            generate_table()
        ],
    )

@app.callback(
    Output('top-section-container', 'children'),
    [Input(str(n), 'n_clicks') for n in range(len(show_users(engine)))]
)

def displayClick(*email):
    ctx = dash.callback_context
    email_id = int(ctx.triggered[0]['prop_id'].split('.')[0])
    user_data = list(show_users(engine))[email_id]
    email = list(user_data.values())[2]
    del_user(email, engine)
      
    return [
        html.Thead(
            children=[
                generate_user_list_header()
            ],
        ),
        generate_table()
    ]