# Core Dash modules
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Just in case
import pandas as pd
import numpy as np

# Connect to app.py file
from app import app
from app import server

# Adding Progression Multiplication functionality

# Connect to other app pages
from apps import home, approach, catalog
from algorithms import alg_chordprogmult

# Index Components

github_profile_pic = "https://avatars1.githubusercontent.com/u/10263186?s=460&u=92a0ab05fe989c7aa4b5a07e5b8d8c8737dba4a1&v=4"

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=github_profile_pic, height="40px")),
                    dbc.Col(dbc.NavbarBrand("/chord-prog-mult", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
            style = {'padding-left' : '5%'}
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse([
                dbc.NavItem(dbc.NavLink("Home", href="/", style = {'color': 'white'})),
                dbc.NavItem(dbc.NavLink("Catalog", href="/catalog", style = {'color': 'white'})),
                dbc.NavItem(dbc.NavLink("Approach", href="/approach", style = {'color': 'white'})),
                dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/Warpyn/chord-prog-mult", style = {'color': 'white'})),
            ],
            id="navbar-collapse",
            navbar=True,
        ),
    ],
    color="#343a40",
    dark=True,
    expand='md',
)

# Index App Layout (the part that stays the same regardless of page)

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    # Bootstrap navbar
    navbar,
    html.Div(id='page-content', children=[])
])


# Callbacks

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
)
def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/approach':
        return approach.layout
    if pathname == '/catalog':
        return catalog.layout
    else:
        return 'Error 404. Page Not Found.'

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
