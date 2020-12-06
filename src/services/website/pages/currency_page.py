import sys
from datetime import timedelta

from dash.dependencies import Output, Input
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


def get_history_data(currency_name):
    for table in CurrencyTables:
        print(currency_name)
        if table.name == currency_name:
            currency = table
            break

    df = get_currency_data(currency, days_step=1)
    last_date = df['unix_timestamp'][len(df) - 1]
    week_interval = last_date - timedelta(weeks=30)
    week_df = df[df['unix_timestamp'] > week_interval]
    return week_df


def get_future_data(currency_name):
    for table in CurrencyTables:
        if table.name == currency_name + '_PRED':
            currency = table
            break
    df = get_currency_data(currency, hours_step=1)
    return df


def create_time_series(historical_data, future_data, currency_name):
    historical_time = historical_data['unix_timestamp']
    historical_values = historical_data['close']

    future_time = future_data['unix_timestamp']
    future_values = future_data['value']

    data = [
        go.Scatter(
            x=historical_time,
            y=historical_values,
            name="Historical data",
            line=dict(color="#C70039"),
            textposition="bottom center"
        ),
        go.Scatter(
            x=future_time, y=future_values,
            name="Prediction",
            line=dict(color="#FFC300"),
            textposition="bottom center"
        )
    ]
    layout = dict(
        title=f'Изменения курса {currency_name}',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dcc.RangeSlider(
                id='currency-slider-id',
            ),
            paper_bgcolor='rgb(233,233,233)',
            type='date'
        )
    )

    return {
        'data': data,
        'layout': layout
    }


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
    hist_titles = ['day', 'week', '1 m.', '6 m.']

    fig = go.Figure()
    for idx, val in enumerate(hist_values):
        fig.add_trace(go.Indicator(
            mode='delta',
            value=last_value - val,
            domain={
                'row': idx // 2,
                'column': idx % 2
            },
            title=f'Delta per {hist_titles[idx]}'
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


def create_bbox_plots(historical_data):
    data = []
    last_hist_date = historical_data['unix_timestamp'].iloc[-1]
    month_delta = timedelta(days=30)
    names = ['last 1 m.', 'last 2 m.', 'last 3m.']

    for i in range(3):
        interval_end = last_hist_date - i * month_delta
        interval_begin = last_hist_date - (i + 1) * month_delta

        data.append(go.Box(
            y=historical_data['close'][
                (historical_data['unix_timestamp'] < interval_end) &
                (historical_data['unix_timestamp'] > interval_begin)
                ],
            boxpoints='outliers',

            name=names[i]
        ))
    layout = {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'showlegend': False
    }
    return go.Figure(data, layout=layout)


# @app.callback(
#     Output('slider-output-container', 'children'),
#     [Input('currency-slider-id', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)


def layout(currency_name):
    # if current_user.is_authenticated:
    hist_data = get_history_data(currency_name)
    future_data = get_future_data(currency_name)

    return html.Div([
        dbc.Row(
            dbc.Col([
                html.Div(id='slider-output-container'),
                html.H4(f"{currency_name}"),
                dcc.Graph(
                    id='prediction-plot',
                    figure=create_time_series(
                        hist_data, future_data,
                        currency_name
                    )
                )
            ])
        ),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='box_plots',
                    figure=create_bbox_plots(hist_data)
                )
            ], className="col-sm"),
            html.Div([
                dcc.Graph(
                    id='indicator',
                    figure=create_indicators(hist_data)
                )
            ], className="col-sm")
        ], className="container row", id='full_div'),
    ])
