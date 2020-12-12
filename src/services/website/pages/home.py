import sys
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
sys.path.append("./../../../../stockx-release")
from src.modules.db_helpers.helper import get_currency_tables_pairs, get_border_rate

home_login_alert = dbc.Alert(
    'User not logged in. Taking you to login.',
    color='danger'
)

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/solar.csv'
)


def layout():
    return build_main_layout()


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def generate_metric_row(col1, col2, col3, col4, col5, header=True):
    if header:
        return html.Tr(children=[
            html.Th(scope="col", children=col1),
            # html.Th(scope="col", children=col2),
            html.Th(scope="col", children=col3),
            html.Th(scope="col", children=col4),
            html.Th(scope="col", children=col5),
        ])
    else:
        return html.Tr(children=[
            html.Th(scope="col", children=col1),
            # html.Td(children=col2),
            html.Td(children=col3),
            html.Td(children=col4),
            html.Td(dbc.NavLink("Подробнее", href=col5)),
        ])


def generate_table():
    result = []
    currencies = get_currency_tables_pairs()
    for currency_name in currencies.keys():
        changes = "TEST"
        current_rate = get_border_rate(
            currencies[currency_name]['historical'], False
        )
        future_rate = get_border_rate(
            currencies[currency_name]['prediction'], True
        )
        button = f"/currencies/{currency_name}"

        # current_indicator = go.Figure(go.Indicator(
        #     mode="number+delta",
        #     value=current_rate,
        #     delta={"reference": current_rate, "valueformat": ".0f"},
        #     #domain={'y': [0, 1], 'x': [0.25, 0.75]}
        # ))

        result.append(generate_metric_row(
            currency_name, changes,
            current_rate,
            future_rate, button, False
        ))
    return html.Tbody(children=result)


def generate_metric_list_header():
    return generate_metric_row(
        'Валюта', 'Изменения за день',
        'Текущий курс($)', 'Курс($) через 40 дней', ''
    )


def build_main_layout():
    return html.Table(
        id="top-section-container",
        className="table",
        children=[
            # Metrics summary
            html.Thead(
                children=[
                    generate_metric_list_header()
                ],
            ),
            generate_table()
        ],
    )
