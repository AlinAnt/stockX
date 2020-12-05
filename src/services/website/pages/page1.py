import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
import random
from flask_login import current_user
import time
from functools import wraps
import datetime
from server import app
from datetime import timedelta
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

import sys
sys.path.append("./../../../../stockx-release")
from src.modules.db_helpers.helper import get_currency_data
from src.modules.db_helpers.config import CurrencyTables

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)
def update_history_data():
    global history_time, history_values
    df = get_currency_data(CurrencyTables.BTC, hours_step=1)
    last_date = df['unix_timestamp'][len(df) - 1]
    week_interval = last_date - timedelta(weeks=30)
    week_df = df[df['unix_timestamp'] > week_interval]
    history_time = week_df['unix_timestamp']
    history_values = week_df['close']
    print(df)

def update_future_data():
    global future_time, future_values
    df = get_currency_data(CurrencyTables.BTC_PRED, hours_step=1)
    future_time = df['unix_timestamp']
    future_values = df['value']
    

update_history_data()
update_future_data()
fig = go.Figure([go.Scatter(x=history_time, y=history_values, name="Now", line=dict(color="#C70039")),
                go.Scatter(x=future_time, y=future_values, name="Prediction", line=dict(color="#FFC300"))])
fig.update_xaxes(
    rangeslider_visible=True,
)
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    
)





location = dcc.Location(id='page1-url',refresh=True)

def layout():
    #if current_user.is_authenticated:
    return html.Div([
        dbc.Row(
            dbc.Col([
                html.H4("Bitcoin"),
                dcc.Graph(id='prediction-plot', figure=fig)
            ])
        ),
        
        dbc.Row([
            dbc.Col([
             #   dcc.Graph(figure=fig_change_day)
            ]),
            dbc.Col([
              #  dcc.Graph(figure=fig_change_week)
            ]),
            dbc.Col([
             #   dcc.Graph(figure=fig_change_day)
            ]),
            dbc.Col([
             #   dcc.Graph(figure=fig_change_day)
            ])
        ]),

        dbc.Row([])

    ])
       




def page1_test_update(trigger):
    '''
    updates iframe with example.com
    '''    
    time.sleep(2)
    return 'http://example.com/'

