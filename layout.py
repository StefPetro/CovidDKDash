import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from preprocessing import cases_by_sex_processing
from plots import *

cases_by_sex = cases_by_sex_processing()


quick_style = {'marginTop': '1vh', 'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '1vh'}

daily_style = {'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '1vh'}

map_style = {'height': '80vh',
             'marginBottom': '1vh', 'marginRight': '0.5vh', 'marginLeft': '1vh'}

stat_style = {'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '1vh'}


dash_layout = html.Div([
    dcc.Location(id='url'),

    dbc.Row(  # Quick overview
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dcc.Markdown('#### Total numbers since the 26th of February')
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(id='daily_info_columns')
                            ]
                        )
                    ],
                    style=quick_style
                )
            )
        ],
        no_gutters=True
    ),

    dbc.Row(  # The daily infected
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Graph(id='daily-plot',
                                      config={"displayModeBar": False})
                        ]
                    ),
                    style=daily_style
                )
            )
        ],
        no_gutters=True
    ),

    dbc.Row(  # Map of municipalities and plot the infections
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(id='map-plot',
                                  style={'height': '100%'},
                                  config={"displayModeBar": False}
                                  ),
                    ]), style=map_style,
                ),
                width=6
            ),

            dbc.Col(

                width=6
            )
        ],
        no_gutters=True
    ),

    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Select(id='stat-select',
                                       value=bar_cases_by_sex(cases_by_sex)
                                       ),

                            dcc.Graph(id='stat-plot',
                                      style={'height': '100%'},
                                      config={"displayModeBar": False},
                                      ),
                        ]
                    ),
                    style=stat_style
                ),
                width='12'
            ),
        ],
        no_gutters=True
    ),

], className='dash-bootstrap')
