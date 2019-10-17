import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from app import df

# Transform data frame to dash data table

app = dash.Dash(__name__)

layout_home = dash_table.DataTable(
    id='table',
    columns=[{'name': i, 'id': i} for i in df.columns],
    data=df.to_dict('records')
)





