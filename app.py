import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_daq as daq
import plotly.io as pio
from statsmodels.tsa import arima_model
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from models import figure_transformation
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        return render_template('upload.html', shape=df.shape)
    return render_template('upload.html')


df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])



# Define dash App
app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])


# Define Layout
def get_options(list):
    dict_list = []
    for i in list:
        dict_list.append({'label': i, 'value': i})

    return dict_list


stocknames = {}
for i in df['stock'].unique():
    stocknames[i] = i

app.layout = html.Div(
    children=[
        html.Div(
            className='row',
            children=[
                # Column for user controls
                html.Div(
                    className='four columns div-user-controls',
                    children=[
                        html.H2('DASH - STOCK PRICES'),
                        html.P('''
                        Visualizing time series'''
                        ),
                        # Dropdown for stock selection
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
                                             multi=True, value=['AAPL'], style={'backgroundColor': '#1E1E1E',
                                                                                'color': 'red'}, className='stockselector'
                                ),
                            ],
                        style={'color': '#1E1E1E'}),
                        # Dropdown for model selection
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='transformationselector', options=get_options(['Log', 'LogDiff',
                                                                                               'Diff']),
                                             multi=False,
                                             placeholder='Select transformation...',
                                             style={'backgroundColor': '#1E1E1E'}
                                             ),
                                dcc.Dropdown(id='periodselector', options=get_options(['1', '2', '3', '4', '5', '6',
                                                                                       '7', '8', '9', '10', '11' , '12']),
                                             multi=False,
                                             placeholder='Select transformation...',
                                             style={'backgroundColor': '#1E1E1E'}
                                             ),


                            ],
                        ),

                    ],
                ),
                html.Div(
                    className='eight columns div-for-charts bg-grey',
                    children=[
                            dcc.Graph(id='timeseries', config={'displayModeBar': False}),
                            html.Div(
                                className='text-padding',
                                children=[
                                    'Select Range',
                                    dcc.RangeSlider(id='range', updatemode='mouseup',
                                                   min=0, max=len(df) - 1, value=[0, len(df) - 1], allowCross=False),
                                ],
                            ),

                            dcc.Graph(id='change', config={'displayModeBar': False}),
                            dcc.Graph(id='transformation', config={'displayModeBar': False}),
                    ],
                ),
            ],
        )
    ]
)


# Callback for timeseries price
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value'),
               Input('range', 'value')])
def update_graph(selected_dropdown_value, value):
    trace1 = []
    df_sub = df[value[0]:value[1]]
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                               paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True
            ),

              }

    return figure


# Callback for timeseries daily change
@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value'),
               Input('range', 'value'),])
def update_change(selected_dropdown_value, value):
    trace1 = []
    df_sub = df[value[0]:value[1]]
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['change'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
              ),

              }

    return figure


# Callback from script
@app.callback(Output('transformation', 'figure'),
              [Input('stockselector', 'value'),
               Input('transformationselector', 'value'),
               Input('range', 'value'),
               Input('periodselector', 'value')])
def update_transformation(selected_stock, selected_transformation, value, periods, df=df):
    return figure_transformation(selected_stock=selected_stock, selected_transformation=selected_transformation,
                        value=value, periods=periods, df=df)


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
