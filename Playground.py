import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_daq as daq
from dash.dependencies import Input, Output, State

# Load Data






# Generate Dash table from data
def generate_datatable(dataframe, max_rows=10):
    datatable = dash_table.DataTable(id='Diamonds Dataset',
                                     columns=[{'name': i, 'id': i} for i in df.columns],
                                     data=df.to_dict('records'),
                                     fixed_rows={'headers': True},
                                     style_cell={'width': '100px', 'maxWidth': '100px', 'minWidth': '100px'}
                                     )
    return datatable


# Generate df so it won't reload every time the div is collapsed
# Loading still slow
datatable_diamonds = generate_datatable(df)

# Stylesheet

# Define dash App
app = dash.Dash(__name__)

# Define Layout
app.layout = html.Div([
    html.H1(children='Dash App'),
    html.Div(children='''An APP in Dash'''),
    html.H4(children='Life Expectancy by GDP'),
    daq.BooleanSwitch(
        id='boolswitch',
        on=False
    ),

    html.Div(id='switch-table'),

    # Markdown text
    dcc.Markdown(children='''
    *Can't display images in Markdown*

    `<img src='assets/diamond.jpg'>`

    But with an absolute path to the asset:

    `html.Img(src=app.get_asset_url('assets/IMAGE.jpg')`
    '''
                 ),
    # Custom dash_core_components graph

])

@app.callback(
    Output('switch-table', 'children'),
    [Input('boolswitch', 'on')],
)
def update_output(on):
    if on is True:
        children = datatable_diamonds
    else:
        children = ''
    return children


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)