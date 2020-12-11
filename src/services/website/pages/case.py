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
from server import app
from sqlalchemy.sql import and_, select

case_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)
 
def all_currencies(case):
    res = []
    for k in case:
        res.append(k.name)
    return '\n'.join(res)

def layout():
    return dbc.Row(html.H4(all_currencies(current_user.case.currencies)))

@app.callback(
    Output('case-trigger','children'),
    [Input('case-test-trigger','children')]
)
def case_test_update(trigger):
    '''
    updates arbitrary value on case page for test
    '''    
    time.sleep(2)
    return html.Div('after the update',style=dict(color='red'))
