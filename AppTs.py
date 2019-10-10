
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_daq as daq
from app import df
from dash.dependencies import Input, Output, State


#%%

df = pd.read_csv('data/stockdata2.csv', index_col=0)

# gets list of stocks to choose from and returns list of dicts with label and value and dict
# and a dictionary with names
def get_options(list):
    dict_list = []
    stocknames = {}
    for i in list:
        dict_list.append({'label': i, 'value': i})
        stocknames[i] = i

    return dict_list, stocknames


layout = html.Div([
    html.H1('Stock Prices', style={'textAlign': 'center'}),
    dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()[0]),
                 multi=True, value=['AAPL'], style={'display': 'block', 'margin-left': 'auto',
                 'margin-right': 'auto', 'width': '60%'}
                 ),
    dcc.Graph(id='timeseries')
], className='container')

@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = get_options(df['stock'].unique())[1]
    trace1 = []
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df[df['Stock'] == stock]['Date'],
                                 y=df[df['Stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056']),
              }

    return figure




df = pd.read_csv('data/stockdata2.csv')
fig = go.Figure()
for name in pd.unique(df['stock']):
    fig.add_trace(go.Scatter(x=df[df['stock']==name]['Date'],
                             y=df[df['stock']==name]['value'],
                             name=name))

fig.show()