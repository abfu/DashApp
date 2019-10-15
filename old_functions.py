# Callback for Timeseries model
def update_model2(selected_dropdown_value, selected_model):
    trace1 = []

    if selected_model is 'arima1':
        forecast = []

    for stock in selected_dropdown_value:
        trace1.append(go.Scatter())

    data = []
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250
              ),

              }

    return figure


dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
             multi=True, value=['AAPL'],
             className='nav-link dropdown'
             ),

app.layout = html.Div([
    html.Div([
    # Header
    html.H1('Stock Prices', style={'textAlign': 'center'}),

        # Multi-Dropdown for stock selection
        dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
                     multi=True, value=['AAPL']
                     ),

        # Dropodown for model selection
        dcc.Dropdown(id='modelselector', options=get_options(['30D', 'arima2', 'arima3']),
                     multi=False, style={'display': 'table', 'margin-left': 'auto',
                                                        'margin-right': 'auto', 'width': '60%'}
                     ),

        dcc.RangeSlider(id='range', updatemode='mouseup',
                        min=0, max=len(df)-1, value=[0, len(df)-1], allowCross=False),

        # Timeseries price
        dcc.Graph(id='timeseries', config={'displayModeBar':False}, style={'hight': '50%', 'margin-top': '0'}),

        # Timeseries daily change
        dcc.Graph(id='change', config={'displayModeBar': False}, style={'hight': '25%'}),

        ], className='container', style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div([
        # Timeseries model
        dcc.Graph(id='model', config={'displayModeBar': False})
    ], style={'width': '49%', 'display': 'inline-block'})
])