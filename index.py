import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, layout_app
from home import app, layout_home
import dash

app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dcc.Link('Data', href='/home'),
    html.Br(),
    dcc.Link('App', href='/app'),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname =='/app':
        return layout_app

    if pathname =='/home':
        return layout_home


    else:
        return '404'

# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
