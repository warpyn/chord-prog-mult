import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

from app import app
from algorithms import alg_chordprogmult

# --- Home Page Layout ---

layout = html.Div(
    [
        html.H1(children = 'Chord Progression Multiplication'),
        dcc.Markdown('''
            With the help of abstract algebra, certain chord progressions can undergo multiplication. This website provides a calculator to multiply custom chord progressions below and an interactive catalog on the [Catalog](/catalog) page to multiply chord progressions found in music. To read more about the mathematical reasoning behind the multiplication idea, visit the [Approach](/approach) page.
        '''),
        html.Hr(),
        html.H3(children = 'Rules'),
        dcc.Markdown(
            children = ['''
                When multiplying two chord progressions, there are a few rules to follow.

                1. In a progression, **no chord may appear more than once**.
                2. To avoid an output equal to the input, both progressions should share at least one chord.

                To Note:

                - This program multiplies progressions in the same direction as function compositions like *f(g(x))*: right to left.
                - Multiplication from left to right is equivalent to *g(f(x))*, which the program's output also includes.
            '''],
            style = {'font-family':'Georgia'}
        ),
        html.Hr(),
        html.H2(children = 'Calculator'),
        dcc.Markdown('''Enter two chord progressions below, where chords are separated by a single space.'''),
        html.Br(),

        # Side by Side Inputs

        html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Markdown(children = '''**Progression *f*:**'''),
                    dbc.Input(id="prog_f", placeholder="e.g. C G", type="text"),
                ]),
                dbc.Col([
                    dcc.Markdown(children = '''**Progression *g*:**'''),
                    dbc.Input(id="prog_g", placeholder="e.g. F Bb C", type="text"),
                ]),
            ]),
        ]),
        html.Br(),
        dbc.Col(
            [
                dbc.Button("Multiply", outline=False, color="primary", block=True, id="mult_button", className="mr-1", type='button'),
            ],
            style = {'padding-right':'0px', 'padding-left':'0px'},
            xs=12, sm=12, md=12, lg=6, xl=3
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown('''**Output:**'''),
        html.Br(),
        html.Div(children = [], id="output_fg", style = {'font-family':'Courier',
        'font-size':'1.15rem'
            }
        ),
        html.Br(),
        html.Div(children = [], id="output_gf", style = {'font-family':'Courier',
        'font-size':'1.15rem'
            }
        ),
        html.Br(),
        html.Br(),

    ],
    style = {'padding-left' : '10%',
            'padding-right' : '10%',
            'padding-top' : '5%'},
)

@app.callback(
    [Output("output_fg", "children"),
    Output("output_gf", "children")],
    [Input("mult_button", "n_clicks")],
    [State("prog_f", "value"),
    State("prog_g", "value")],
    prevent_inital_call = True
)
def update_output(n, progf_chosen, progg_chosen):
    if progf_chosen == None or progg_chosen == None:
        raise dash.exceptions.PreventUpdate
    elif len(progf_chosen) > 0 and len(progg_chosen) > 0 and n > 0:
        product_fg = alg_chordprogmult.chordProgMult(progf_chosen, progg_chosen)
        product_gf = alg_chordprogmult.chordProgMult(progg_chosen, progf_chosen)
        equation_fg = f"(f)(g) = ({progf_chosen})({progg_chosen}) = {product_fg}"
        equation_gf = f"(g)(f) = ({progg_chosen})({progf_chosen}) = {product_gf}"
        return [equation_fg], [equation_gf]
    else:
        raise dash.exceptions.PreventUpdate
