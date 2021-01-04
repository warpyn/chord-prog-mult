import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pathlib

import pandas as pd
import numpy as np

from app import app
from algorithms import alg_chordprogmult

# Read CSV into pandas dataframe
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath("prog_catalog.csv"))
dff = df.copy() # for the "selected" table

# --- Catalog Page Layout ---

layout = html.Div([
        html.H1(children='Catalog'),
        dcc.Markdown('''
            Below is a catalog of chord progressions used in music that follow the rules mentioned on the home page. Select any two progressions from the catalog to multiply them and view the output. Multiplication options for chord symbols as well as roman numerals are included.
        '''),
        html.Br(),
        dbc.RadioItems(
            options=[
                {"label": "Chord Letter Symbols (e.g. \"Dm G C\")", "value": 3},
                {"label": "Roman Numeral Analysis (e.g. \"ii V I\")", "value": 4},
            ],
            value=3,
            id="chord-display-input",
            style = {'font-family':'Georgia'},
        ),
        html.Br(),
        dash_table.DataTable(
            id = 'catalog',
            columns = [
                {"name": i, "id": i} for i in df.columns
            ],
            data = df.to_dict('records'),
            filter_action = "native", # searchable columns to find songs
            sort_action = "native", # data in a column can be sorted
            sort_mode = "single",
            row_selectable = "multi", # selecting progressions
            row_deletable = False,
            selected_rows = [],
            page_action = "native",
            page_current = 0,
            page_size = 11,
            style_data = {
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_table = {
                'overflowX': 'auto'
            },
            style_cell = {
                'textAlign':'left',
                'fontSize':16,
                'font-family':'Courier',
            }
        ),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.H3(children = 'Selected Progressions'),
        html.Div(children = [], id="selected-output"),
        html.Br(),
        dbc.Col(
            [
                dbc.Button("Multiply", outline=False, color="primary", block=True, id="catalogmult_button", className="mr-1", type='button'),
            ],
            style = {'padding-right':'0px', 'padding-left':'0px'},
            xs=12, sm=12, md=12, lg=6, xl=3
        ),
        html.Br(),
        html.Hr(),
        html.H3(children = 'Output'),
        html.Br(),
        html.Div(children = [], id="catalog-mult-output-fg",
        style = {'font-family':'Courier', 'font-size':'1.15rem'}
        ),
        html.Br(),
        html.Div(children = [], id="catalog-mult-output-gf",
        style = {'font-family':'Courier', 'font-size':'1.15rem'}
        ),
        html.Br(),
        html.Br(),

    ],
    style = {'padding-left' : '10%',
            'padding-right' : '10%',
            'padding-top' : '5%'},
)

@app.callback(
    [Output('selected-output', 'children')],
    [Input('catalog', 'selected_rows'),
    Input('chord-display-input', 'value')],
)
def update_selected(rows_chosen_ids, display_type_num):
    dff = df.copy()
    dff = dff.iloc[rows_chosen_ids, [0, 1, 2, display_type_num]]
    selected_table = dash_table.DataTable(
        id = 'selected',
        columns = [
            {"name": i, "id": i} for i in dff.columns
        ],
        data = dff.to_dict('records'),
        filter_action = "none",
        sort_action = "none",
        row_selectable = False,
        row_deletable = False,
        page_action = "native",
        page_current = 0,
        page_size = 5,
        # style_data = {
        #     'whiteSpace': 'normal',
        #     'height': 'auto'
        # }
        style_table = {
            'overflowX': 'auto'
        },
        style_cell = {
            'textAlign':'left',
            'fontSize':16,
            'font-family':'Courier'
        }
    )
    return [selected_table]

@app.callback(
    [Output('catalog-mult-output-fg', 'children'),
    Output('catalog-mult-output-gf', 'children')],
    [Input('catalogmult_button', 'n_clicks')],
    [State('catalog', 'selected_rows'),
    State('chord-display-input', 'value')],
    prevent_inital_call = True
)
def update_catalog_multoutput(n, rows_chosen_ids, display_type_num):
    num_chosen_rows = len(rows_chosen_ids)
    if n == 0 or num_chosen_rows == 0:
        raise dash.exceptions.PreventUpdate
    if num_chosen_rows == 2:
        dfg = df.copy()
        dfg = dfg.iloc[rows_chosen_ids, [display_type_num]]
        prog_f_selected = dfg.iloc[0,0]
        prog_g_selected = dfg.iloc[1,0]
        product_fg = alg_chordprogmult.chordProgMult(prog_f_selected, prog_g_selected)
        product_gf = alg_chordprogmult.chordProgMult(prog_g_selected, prog_f_selected)
        equation_fg = f"({prog_f_selected})({prog_g_selected}) = {product_fg}"
        equation_gf = f"({prog_g_selected})({prog_f_selected}) = {product_gf}"
        return [equation_fg], [equation_gf]
    elif num_chosen_rows > 2:
        return ["Error: More Than 2 Progressions Selected"], ["Select exactly two progressions to multiply."]
    elif num_chosen_rows == 1:
        return ["Error: Less Than 2 Progressions Selected"], ["Select exactly two progressions to multiply."]
    else:
        raise dash.exceptions.PreventUpdate
