import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from plots import *

stat_select_options = [
    {'label': 'Daily infected',
     'value': 'daily_infected'},
    {'label': 'Cases by sex for different age groups',
     'value': 'cases_by_sex'},
    {'label': 'Deaths over time',
     'value': 'deaths_over_time'},
    {'label': 'Cumulative deaths since March 11th',
     'value': 'cumulative_deaths'}

]


quick_style = {'marginTop': '1vh', 'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '1vh'}

daily_style = {'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '1vh'}

map_style = {'height': '80vh',
             'marginBottom': '1vh', 'marginRight': '0.5vh', 'marginLeft': '1vh'}

muni_style = {'height': '80vh',
              'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '0.5vh'}

stat_style = {'marginBottom': '1vh', 'marginRight': '1vh', 'marginLeft': '1vh'}

nav_links = dbc.Row(
    [
        dbc.Col(
            html.A(
                dbc.Button("Data source", color="light", outline=True),
                href='https://covid19.ssi.dk/overvagningsdata/download-fil-med-overvaagningdata',
                target='_blank',
                className="ml-2"
            ),
            width='auto'
        )
    ],
    no_gutters=True,
    # className="ml-auto flex-nowrap mt-3 mt-md-0",  # Move links to the left in nav bar
    align="center",
)

dash_layout = html.Div([
    dcc.Location(id='url'),

    dbc.Navbar(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src='assets/navbaricon.svg', height="30px")
                    ),
                    dbc.Col(
                        dbc.NavbarBrand("Covid-19 Denmark", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(nav_links, id="navbar-collapse", navbar=True),
        ],
        color='dark',
        dark=True
    ),

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
                            dbc.Select(id='stat-select',
                                       options=stat_select_options,
                                       value='daily_infected'
                                       ),
                            dcc.Loading(
                                dcc.Graph(id='stat-plot',
                                          config={"displayModeBar": False}),
                                type='dot'
                            ),
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
                    dbc.CardBody(
                        dcc.Graph(id='map-plot',
                                  style={'height': '100%'},
                                  config={"displayModeBar": False}
                                  ),

                    ),
                    style=map_style,
                ),
                width=6
            ),

            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(id='municipality-plot',
                                  style={'height': '100%'},
                                  config={"displayModeBar": False}
                                  ),
                    ]),
                    style=muni_style,
                ),
                width=6
            )
        ],
        no_gutters=True
    ),

], className='dash-bootstrap')
