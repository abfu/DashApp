import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np


#%%
def figure_model(selected_stock, selected_value, value, df):
    trace1 = []
    trace2 = []
    df_sub = df[value[0]:value[1]]
    for stock in selected_stock:
        df_win = df_sub.loc[df_sub['stock'] == stock].rolling('30D').mean()
        if value[1] > len(df_sub):
            value[1] = len(df_sub)
        trace1.append(go.Scatter(x=df_win.index,
                                 y=np.log(df_win['value']),
                                 name=stock))
        #trace2.append(go.Scatter(x=df_win.index,
         #                        y=ARIMA(np.log(df_win['value']), order=(1, 0, 1)).fit(disp=-1).fittedvalues,
          #                               name='Arima ' + stock))
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