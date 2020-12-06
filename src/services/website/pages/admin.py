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


def layout():
    return html.Div([
        html.H4(f'Hi,{current_user.role}'),
       
    ])