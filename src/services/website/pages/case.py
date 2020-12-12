import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash import no_update
from dash.dependencies import Input, Output, State
from flask_login import current_user
from server import app, User
from sqlalchemy.sql import and_, select
from utilities.auth import del_currency

case_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)
 
def layout():
    return html.Div([
        #html.Div(id='curr-div', display=None),
        build_main_layout()
    ])

def generate_curr_row(col1, col2, header=True):
    if header:
        return html.Tr(children=[
            html.Th(scope="col", children=col1),
            html.Th(scope="col", children=col2),
           
        ])
    else:
        return html.Tr(children=[
           html.Th(scope="col", children=col1),
           html.Td(dbc.NavLink("More details", href=col2)),
        ])


def generate_table():
    res = []
    case = current_user.case.currencies
    for currency in case:
        #print(currency)
        curr_name = currency.name
        button = f"/currencies/{curr_name}"

        res.append(generate_curr_row(
            curr_name, button, False
        ))
    return html.Tbody(children=res)




def generate_curr_list_header():
    return generate_curr_row(
        'Currency name', '', True
    )

def build_main_layout():
    return html.Table(
        id='top-container',
        className="table",
        children=[
            html.Thead(
                children=[
                    generate_curr_list_header()
                ],
            ),
            generate_table()
        ],
    )





















