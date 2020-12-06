import sys
from datetime import timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

sys.path.append("./../../../../stockx-release")
from src.modules.db_helpers.helper import get_currency_data
from src.modules.db_helpers.config import CurrencyTables

login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)


def get_history_data():
    df = get_currency_data(CurrencyTables.BTC, days_step=1)
    last_date = df['unix_timestamp'][len(df) - 1]
    week_interval = last_date - timedelta(weeks=30)
    week_df = df[df['unix_timestamp'] > week_interval]
    return week_df


def get_future_data():
    df = get_currency_data(CurrencyTables.BTC_PRED, hours_step=1)
    return df


def create_time_series(historical_data, future_data):
    historical_time = historical_data['unix_timestamp']
    historical_values = historical_data['close']

    future_time = future_data['unix_timestamp']
    future_values = future_data['value']

    fig = go.Figure([
        go.Scatter(
            x=historical_time,
            y=historical_values,
            name="historical_scatter",
            line=dict(color="#C70039"),
            textposition="bottom center"

        ),
        go.Scatter(
            x=future_time, y=future_values,
            name="Prediction",
            line=dict(color="#FFC300"),
            textposition="bottom center"
        )
    ])
    fig.update_xaxes(
        rangeslider_visible=True,
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig.update_traces(
        textposition="bottom center"
    )


    return fig


def create_indicators(historical_data):
    last_value = historical_data['close'].iloc[-1]
    last_hist_date = historical_data['unix_timestamp'].iloc[-1]

    day_ago = historical_data['close'][
        historical_data['unix_timestamp'] == last_hist_date - timedelta(days=1)
        ].iloc[0]

    week_ago = historical_data['close'][
        historical_data['unix_timestamp'] == last_hist_date - timedelta(days=7)
        ].iloc[0]

    month_ago = historical_data['close'][
        historical_data['unix_timestamp'] == last_hist_date - timedelta(days=30)
        ].iloc[0]

    year_ago = historical_data['close'][
        historical_data['unix_timestamp'] == last_hist_date - timedelta(days=180)
    ].iloc[0]

    hist_values = [day_ago, week_ago, month_ago, year_ago]
    hist_titles = ['day', 'week', 'month', '6 months']
    # print(week_ago)
    # print(last_value)
    # print(last_value - week_ago)

    fig = go.Figure()
    for idx, val in enumerate(hist_values):
        fig.add_trace(go.Indicator(
            mode='delta',
            value=last_value - val,
            domain={
                'row': idx // 2,
                'column': idx % 2
            },
            title=f'Change per {hist_titles[idx]}'
        ))

    fig.update_layout(
        grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
        template={
            'data': {
                'indicator': [{
                    'mode': "number",
                    'delta': {
                        'reference': 0
                    }
                }]
            }})
    return fig


#
#
# location = dcc.Location(id='page1-url', refresh=True)
#
# today_value = int(history_values[-1])
# # changes_currency_day
# yesterday_value = int(df["value"][df['datetime'] == (last_date - timedelta(days=1))])
# fig_change_day = go.Figure(go.Indicator(
#     mode="number+delta",
#     value=today_value,
#     number={'prefix': "$"},
#     delta={'position': 'top', 'reference': yesterday_value},
#     domain={'x': [0, 1], 'y': [0, 1]}
#
# ))
# fig_change_day.update_layout(paper_bgcolor="#d3e3f2")
#
# # changes_currency_week
# week_past_value = int(df["value"][df['datetime'] == (last_date - timedelta(weeks=1))])
# fig_change_week = go.Figure(go.Indicator(
#     mode="number+delta",
#     value=today_value,
#     number={'prefix': "$"},
#     delta={'position': 'top', 'reference': week_past_value},
#     domain={'x': [0, 1], 'y': [0, 1]}
#
# ))
# fig_change_week.update_layout(paper_bgcolor="#d3e3f2")


# fig_change_week.update_traces(title_text="Week", selector={type='indicator'})

def layout():
    # if current_user.is_authenticated:
    hist_data = get_history_data()
    future_data = get_future_data()

    return html.Div([
        dbc.Row(
            dbc.Col([
                html.H4("Bitcoin"),
                dcc.Graph(
                    id='prediction-plot',
                    figure=create_time_series(
                        hist_data, future_data
                    )
                )
            ])
        ),
        dbc.Row([
            dcc.Graph(
                id='test_indicator',
                figure=create_indicators(hist_data)
            ),
        ]),


    ])
