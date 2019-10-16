import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np


#%%



def figure_transformation(selected_stock, selected_transformation, value, df, periods=1):
    trace1 = []
    trace2 = []

    # Convert str to int

    try:
        periods = int(periods)

    except:
        periods = 1

    # drop change
    df_sub = df[value[0]:value[1]][['value', 'stock']]


    for stock in selected_stock:

        # Depending on selected transformation, return transformed series
        df_sub_stock = df_sub.loc[df_sub['stock'] == stock]
        if selected_transformation == 'Log':
            df_sub_stock['value'] = np.log(df_sub_stock.loc[:, 'value'])

        elif selected_transformation == 'LogDiff':
            df_sub_stock['value'] = np.log(df_sub_stock.loc[:, 'value']).diff(periods=periods)

        elif selected_transformation == 'Diff':
            df_sub_stock['value'] = df_sub_stock.loc[:, 'value'].diff(periods=periods)

        if value[1] > len(df_sub):
            value[1] = len(df_sub)
        trace1.append(go.Scatter(x=df_sub_stock.index,
                                 y=df_sub_stock['value'],
                                 name=stock))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                      colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                      template='plotly_dark',
                                   paper_bgcolor='rgba(0, 0, 0, 0)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                  hovermode='x',
              ),
              }

    return figure



def figure_graph(selected_dropdown_value, value):
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
