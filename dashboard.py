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
from preprocessing import cases_by_sex_processing
from plots import bar_cases_by_sex

archive = zp.ZipFile('Data-Epidemiologiske-Rapport-08102020-da23.zip', 'r')

muni_test_pos = 'Municipality_test_pos.csv'
municipality_cases = 'Municipality_cases_time_series.csv'

data = archive.open(muni_test_pos)
test_df = pd.read_csv(data, sep=';')
test_df['Kommune_(id)'] = test_df['Kommune_(id)'].astype(str)  # to str so we avoid floats
muni_code_dict = pd.Series(test_df['Kommune_(id)'].values, index=test_df['Kommune_(navn)']).to_dict()
muni_code_dict['Copenhagen'] = '101'

cases_data = archive.open(municipality_cases)
cases_df = pd.read_csv(cases_data, sep=';')
melt_cases = pd.melt(cases_df,
                     id_vars=['date_sample'],
                     value_vars=cases_df.columns[1:],
                     var_name=['commune'],
                     value_name='infected')
cases_sum_df = melt_cases.groupby('commune').sum().reset_index()
cases_sum_df['code'] = cases_sum_df['commune'].map(muni_code_dict)
cases_sum_df['code'] = cases_sum_df['code'].apply(lambda x: str(x).zfill(4))

cases_by_sex = cases_by_sex_processing()


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
    fig = px.choropleth_mapbox(cases_sum_df, geojson=geojson,
                               locations='code',
                               color='infected',
                               featureidkey="properties.KOMKODE",
                               color_continuous_scale="Blues",
                               range_color=(0, 2500),
                               mapbox_style='carto-positron',
                               center={'lat': 55.9397, 'lon': 11.5},  # 'lon': 9.5156
                               zoom=6.5  # 5.6
                               # scope='europe',
                               # projection="mercator",
                               )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      dragmode=False)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=port)
