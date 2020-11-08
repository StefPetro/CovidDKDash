import dash
import pandas as pd
import json
import zipfile as zp
from urllib.request import urlopen
from dash.dependencies import Output, Input, State

# for plotting
import plotly.express as px
import plotly.graph_objects as go

# import layout
from layout import dash_layout

# import preprocessing and plots
from preprocessing import cases_by_sex_processing, cumulative_cases_by_municipality
from plots import bar_cases_by_sex

# Load the data
cases_by_sex = cases_by_sex_processing()
cumulative_cases = cumulative_cases_by_municipality()


with open('mapsGeoJSON/multipoly-kommuner.geojson', encoding='utf-8') as json_file:
    geojson = json.load(json_file)


port = 1337
app = dash.Dash()
app.title = 'Covid-19 Denmark Dashboard'
app.layout = dash_layout


@app.callback(
    Output('top-select', 'options'),
    [Input('url', 'pathname')]
)
def update_top_select(url):
    options = [
        {'label': 'Cases by sex for different age groups',
         'value': bar_cases_by_sex(cases_by_sex)}
    ]
    return options


@app.callback(
    Output('top-stat-plot', 'figure'),
    [Input('top-select', 'value')]
)
def update_top_plot(select):
    # alternative solution
    # less imports from different files
    # if select == 'cases_by_sex':
    #    return bar_cases_by_sex(cases_by_sex)
    # elif ...

    return select


@app.callback(
    Output('map-plot', 'figure'),
    [Input('url', 'pathname')]
)
def update_map_plot(url):

    fig = go.Figure(
        go.Choroplethmapbox(geojson=geojson,
                            locations=cumulative_cases['code'],
                            z=cumulative_cases['infected'],
                            text=cumulative_cases['municipality'],
                            hovertemplate="Municipality: %{text} <br>Infected: %{z} <extra></extra>",
                            colorscale='Inferno_r',
                            featureidkey="properties.KOMKODE",
                            zmin=0,
                            zmax=6500)
    )

    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=5.6,
                      mapbox_center={'lat': 55.9397, 'lon': 11.5},
                      hoverlabel={'font_size': 16},)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=port)
