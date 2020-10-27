import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from preprocessing import cases_by_sex_processing
from plots import bar_cases_by_sex

cases_by_sex = cases_by_sex_processing()


map_style = {'height': '97vh', 'marginTop': '1vh', 'box-shadow': '2px 2px 2px lightgrey',
             'marginBottom': '1vh', 'marginRight': '0.5vh', 'marginLeft': '1vh'}
top_style = {'height': '48vh', 'width': '99vh', 'marginTop': '1vh',
             'marginBottom': '0.5vh', 'marginRight': '1vh', 'marginLeft': '0.5vh'}
bottom_style = {'height': '48vh', 'width': '99vh', 'marginTop': '0.5vh',
                'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '0.5vh'}

dash_layout = html.Div([
    dcc.Location(id='url'),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(id='map-plot',
                              style={'height': '100%'}
                              ),
                ]), style=map_style
            )
        ),

        dbc.Col([
            dbc.Row([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Select(id='top-select',
                                   value=bar_cases_by_sex(cases_by_sex)
                                   ),
                        dcc.Graph(id='top-stat-plot',
                                  style={'height': '100%'}),
                    ]), style=top_style
                )
            ]),
            dbc.Row([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Select(id='bottom-select'),
                        dcc.Graph(id='bottom-stat-plot',
                                  style={'height': '100%'}),
                    ]), style=bottom_style
                ),
            ])
        ])
    ]),

], className='dash-bootstrap')
