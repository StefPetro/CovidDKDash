import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

dash_layout = html.Div([
    dcc.Location(id='url'),
    dbc.Card(
        dbc.CardBody([
            dbc.Spinner(
                dcc.Graph(id='map-plot',
                          style={'height': '94vh'}),
                fullscreen=True
            ),
        ]), style={'width': '50%',
                   'marginTop': 10, 'marginBottom': 10, 'marginRight': 10, 'marginLeft': 10}
    )
])

