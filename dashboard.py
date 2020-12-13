import dash
import pandas as pd
import json
import zipfile as zp
from urllib.request import urlopen

from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# for plotting
import plotly.express as px
import plotly.graph_objects as go

# import layout
from layout import dash_layout

# import preprocessing and plots
from preprocessing import *
from plots import bar_cases_by_sex

# Load the data
cases_by_sex = cases_by_sex_processing()
cumulative_cases = cumulative_cases_by_municipality()


with open('data/mapsGeoJSON/multipoly-kommuner.geojson', encoding='utf-8') as json_file:
    geojson = json.load(json_file)


port = 1337
app = dash.Dash()
app.title = 'Covid-19 Denmark Dashboard'
app.layout = dash_layout


@app.callback(
    Output('stat-select', 'options'),
    [Input('url', 'pathname')]
)
def update_stat_select(url):
    options = [
        {'label': 'Cases by sex for different age groups',
         'value': bar_cases_by_sex(cases_by_sex)}
    ]
    return options


@app.callback(
    Output('stat-plot', 'figure'),
    [Input('stat-select', 'value')]
)
def update_stat_plot(select):
    # alternative solution
    # less imports from different files
    # if select == 'cases_by_sex':
    #    return bar_cases_by_sex(cases_by_sex)
    # elif ...

    return select


@app.callback(
    Output('daily_info_columns', 'children'),
    [Input('url', 'pathname')]
)
def update_daily_info(url):
    columns = []

    total_cases = daily_cases = daily_infected().iloc[:-1, -1].sum()

    columns.append(
        dbc.Col(
            dcc.Markdown(
                f'''
                Confirmed cases:  
                {total_cases}
                '''
            )
        )
    )

    return columns


@app.callback(
    Output('daily-plot', 'figure'),
    [Input('url', 'pathname')]
)
def update_daily_plot(url):
    daily_cases = daily_infected().iloc[:-1, :]

    fig = go.Figure(
        go.Bar(
            x=daily_cases['date_sample'],
            y=daily_cases['total_daily'],
            hovertemplate="Date: %{x} <br>Infected: %{y} <extra></extra>",
        )
    )

    fig.update_layout(
        title_text='Daily infected in Denmark',
        yaxis=dict(
            title='Infected'
        ),
        margin={"r": 10, "t": 50, "l": 10, "b": 20},
    )
    return fig



@app.callback(
    Output('map-plot', 'figure'),
    [Input('url', 'pathname')]
)
def update_map_plot(url):

    min_val = min(cumulative_cases['infected'])
    max_val = max(cumulative_cases['infected'])

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=cumulative_cases['code'],
            z=cumulative_cases['infected'],
            text=cumulative_cases['municipality'],
            hovertemplate="Municipality: %{text} <br>Infected: %{z} <extra></extra>",
            colorscale='Inferno_r',
            featureidkey="properties.KOMKODE",
            zmin=min_val,
            zmax=max_val,
            colorbar=dict(
                exponentformat='none'
            )
        )
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5.6,
        mapbox_center={'lat': 55.9397, 'lon': 11.5},
        hoverlabel={'font_size': 16},
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=port)
