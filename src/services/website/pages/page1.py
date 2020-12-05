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

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

df = pd.read_parquet('data.parquet', engine="pyarrow")
df["datetime"] = pd.to_datetime(df['datetime'])
last_date = df['datetime'][len(df)-1]
week_interval = last_date - timedelta(weeks=60)
week_df = df[df['datetime'] > week_interval]
week_df.iloc[::10080,:]

dk = pd.read_csv("future.csv")
dk["datetime"] = pd.to_datetime(dk['datetime'])
first_date = dk['datetime'][0]
our_interval = first_date + timedelta(weeks=60)
our_dk = dk[dk['datetime'] < our_interval]

fig = go.Figure([go.Scatter(x=week_df["datetime"], y=week_df['value'], name="Now", line=dict(color="#C70039")),
                go.Scatter(x=our_dk['datetime'], y=our_dk['value'], name="Prediction", line=dict(color="#FFC300"))])
fig.update_xaxes(
    rangeslider_visible=True,
)
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    
)
today_value = int(df['value'][len(df)-1])

#changes_currency_day
yesterday_value = int(df["value"][df['datetime'] == (last_date - timedelta(days=1))])
fig_change_day = go.Figure(go.Indicator(
    mode = "number+delta",
    value = today_value,
    number = {'prefix':"$"},
    delta = {'position': 'top', 'reference': yesterday_value},
    domain = {'x': [0, 1], 'y': [0, 1]}

))
fig_change_day.update_layout(paper_bgcolor = "#d3e3f2")

#changes_currency_week
week_past_value =  int(df["value"][df['datetime'] == (last_date - timedelta(weeks=1))])
fig_change_week = go.Figure(go.Indicator(
    mode = "number+delta",
    value = today_value,
    number = {'prefix':"$"},
    delta = {'position': 'top', 'reference': week_past_value},
    domain = {'x': [0, 1], 'y': [0, 1]}

))
fig_change_week.update_layout(paper_bgcolor = "#d3e3f2")
#fig_change_week.update_traces(title_text="Week", selector={type='indicator'})




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
                dcc.Graph(figure=fig_change_day)
            ]),
            dbc.Col([
                dcc.Graph(figure=fig_change_week)
            ]),
            dbc.Col([
                dcc.Graph(figure=fig_change_day)
            ]),
            dbc.Col([
                dcc.Graph(figure=fig_change_day)
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

