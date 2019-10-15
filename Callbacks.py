import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_daq as daq
import plotly.io as pio
from dash.dependencies import Input, Output, State

df = pd.read_csv('data/stockdata2.csv', index_col=0)

app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    dcc.Dropdown(id='dropdown'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

@app.callback(Output('intermediate-value', 'children'),
              [Input('dropdown', 'value')])
def clean_data(value):


if __name__ == '__main__':
    app.run_server(debug=True)
