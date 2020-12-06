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

import pandas as pd
import plotly.graph_objs as go

home_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv'
)

def layout():
    return html.Div([
        html.H4(current_user.role),
        dash_table.DataTable(
            style_cell={
                'whiteSpace':'normal',
                'height':'auto',
            },
            id="main_table",
            columns=[{
                "name": i,
                "id": i} for i in df.columns],
                data=df.to_dict('records'),
        ),
    ])
        


@app.callback(
    Output('home-test','children'),
    [Input('home-test-trigger','children')]
)
def home_test_update(trigger):
    '''
    updates arbitrary value on home page for test
    '''    
    time.sleep(2)
    return html.Div('after the update',style=dict(color='red'))
