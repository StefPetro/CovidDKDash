import dash
import pandas as pd
import json
import zipfile as zp
from urllib.request import urlopen

from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# for plotting
import plotly.express as px
import plotly.graph_objects as go

# import layout
from layout import dash_layout

# import plots
from plots import *

# Load the data
cumulative_cases = municipality_cumulative_cases_data()


with open('data/mapsGeoJSON/multipoly-kommuner.geojson', encoding='utf-8') as json_file:
    geojson = json.load(json_file)


port = 1337
app = dash.Dash()
app.title = 'Covid-19 Denmark Dashboard'
app.layout = dash_layout


@app.callback(
    Output('stat-plot', 'figure'),
    [Input('stat-select', 'value')]
)
def update_stat_plot(select):

    if select == 'daily_infected':
        return daily_infected()
    elif select == 'cases_by_sex':
        return cases_by_sex()
    elif select == 'deaths_over_time':
        return deaths_over_time()
    elif select == 'cumulative_deaths':
        return cumulative_deaths()

    raise PreventUpdate


@app.callback(
    Output('daily_info_columns', 'children'),
    [Input('url', 'pathname')]
)
def update_daily_info(url):
    columns = []

    total_cases = daily_cases = daily_infected_data().iloc[:-1, -1].sum()

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
    Output('municipality-plot', 'figure'),
    [Input('url', 'pathname')]
)
def update_municipality_plot(url):
    muni_infected = municipality_infected_data()

    # Showing top 20
    muni_infected = muni_infected.iloc[:20, :].sort_values('infected', ascending=True)

    fig = go.Figure(
        go.Bar(
            x=muni_infected.infected.values,  # Switch x and y values to get horizontal plot
            y=muni_infected.index,
            orientation='h',
        )
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
