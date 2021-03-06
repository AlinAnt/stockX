# index page
import random

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import redirect
from flask_login import current_user, logout_user
import random
# app pages
from pages import (
    home,
    profile,
    currency_page,
    case,
    admin,
)

# app authentication 
from pages.auth_pages import change_password, forgot_password, login, register
from server import app, server

from src.modules.db_helpers.helper import get_currency_tables_pairs

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("StockX", href="/home"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="/home")),
                    dbc.NavItem(dbc.NavLink("Random coin", href="/random")),
                    dbc.NavItem(dbc.NavLink("Case", href="/case")),
                    dbc.NavItem(dbc.NavLink(id='user-name',href='/profile')),
                    dbc.NavItem(dbc.NavLink("Admin", id='admin_id', href='/admin')),
                    dbc.NavItem(dbc.NavLink('Login',id='user-action',href='Login'))
                ]
            )
        ]
    ),
    className="mb-5",
)



app.layout = html.Div(
    [
        header,
        html.Div(
            [
                dbc.Container(
                    id='page-content'
                )
            ]
        ),
        dcc.Location(id='base-url', refresh=True)
    ]
)


@app.callback(
    Output('page-content', 'children'),
    [Input('base-url', 'pathname')])
def router(pathname):
    '''
    routes to correct page based on pathname
    '''
    # for debug
    #print('routing to',pathname)
    
    # auth pages
    if pathname == '/login':
        if not current_user.is_authenticated:
            return login.layout()
    elif pathname =='/register':
        if not current_user.is_authenticated:
            return register.layout()
    elif pathname == '/change':
        if not current_user.is_authenticated:
            return change_password.layout()
    elif pathname == '/forgot':
        if not current_user.is_authenticated:
            return forgot_password.layout()
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
    
    # app pages
    elif pathname == '/' or pathname=='/home' or pathname=='/home':
        if current_user.is_authenticated:
            return home.layout()
    elif pathname == '/profile' or pathname =='/profile':
        if current_user.is_authenticated:
            return profile.layout()
    elif '/currencies' in pathname:
        if current_user.is_authenticated:
            return currency_page.layout(pathname.split(r'/')[-1])
    elif pathname == '/case' or pathname =='/case':
        if current_user.is_authenticated:
            return case.layout()
    elif pathname == '/random':
        if current_user.is_authenticated:
            currencies = list(get_currency_tables_pairs().keys())
            name = random.choice(currencies)

            return dcc.Location(
                pathname=f"/currencies/{name}",
                id='currency_redirect'
            )
    elif pathname == '/admin' or pathname == '/admin':
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return admin.layout()
            else:
                return home.layout()
                
    # DEFAULT LOGGED IN: /home
    if current_user.is_authenticated:
        return home.layout()
    
    # DEFAULT NOT LOGGED IN: /login
    return login.layout()


@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def profile_link(content):
    '''
    returns a navbar link to the user profile if the user is authenticated
    '''
    if current_user.is_authenticated:
        return html.Div(current_user.first)
    else:
        return ''

@app.callback(
    Output('admin_id', 'children'),
    [Input('page-content', 'children')])
def admin_link(content):
    '''
    returns a navbar link to the user profile if the user is authenticated
    '''
    if current_user.is_authenticated and current_user.role == 'admin':

        return html.Div("Admin")
    else:
        return ''

@app.callback(
    [Output('user-action', 'children'),
     Output('user-action','href')],
    [Input('page-content', 'children')])
def user_logout(input1):
    '''
    returns a navbar link to /logout or /login, respectively, if the user is authenticated or not
    '''
    if current_user.is_authenticated:
        return 'Logout', '/logout'
    else:
        return 'Login', '/login'

if __name__ == '__main__':
    app.run_server(port=8000, debug=False)
