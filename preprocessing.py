import json
import zipfile as zp
import re
import pandas as pd

archive = zp.ZipFile('data/data.zip', 'r')


def cumulative_cases_by_municipality():

    # Open det test csv for municipalities to create a dictionary for the municipalities and their codes.
    muni_test_pos = 'Municipality_test_pos.csv'

    muni_test_data = archive.open(muni_test_pos)
    muni_test_df = pd.read_csv(muni_test_data, sep=';')
    muni_test_df['Kommune_(id)'] = muni_test_df['Kommune_(id)'].astype(str)  # to str so we avoid floats
    muni_code_dict = pd.Series(muni_test_df['Kommune_(id)'].values, index=muni_test_df['Kommune_(navn)']).to_dict()

    # add code for Copenhagen manually, as it is called København in the other files
    muni_code_dict['Copenhagen'] = '101'

    # Open the time series of cases for the municipalities
    municipality_cases = 'Municipality_cases_time_series.csv'

    cases_data = archive.open(municipality_cases)
    cases_df = pd.read_csv(cases_data, sep=';')

    # Melt the dataframe to get three columns, one for date, municipality, and cases.
    melt_cases = pd.melt(cases_df,
                         id_vars=['date_sample'],
                         value_vars=cases_df.columns[1:],
                         var_name=['municipality'],
                         value_name='infected')

    # Group the melted dataframe by the municipality and sum the cases.
    # Create a new column called 'code' by mapping the municipalities with their codes, using muni_code_dict.
    cases_sum_df = melt_cases.groupby('municipality').sum().reset_index()  # Not drop=True as it removes muni
    cases_sum_df['code'] = cases_sum_df['municipality'].map(muni_code_dict)

    # zfill the municipality codes to get the same numbers as in the geojson
    cases_sum_df['code'] = cases_sum_df['code'].apply(lambda x: str(x).zfill(4))

    return cases_sum_df


def cases_by_sex_processing():
    # Open data in archive and load to dataframe
    # use decimal=',' to avoid (european) thousand separator confusion
    cases_by_sex_data = archive.open('Cases_by_sex.csv')
    cases_by_sex = pd.read_csv(cases_by_sex_data, sep=';', decimal=',')

    # Strip whitespace around strings and change columns names
    cases_by_sex.columns = ['age_group', 'women', 'men', 'total']
    cases_by_sex['total'] = cases_by_sex['total'].str.strip().str.replace('.', '').astype(int)
    cases_by_sex['women'] = cases_by_sex['women'].str.strip().str.replace('.', '')
    cases_by_sex['men'] = cases_by_sex['men'].str.strip().str.replace('.', '')

    # Create two new columns from percent data in women and men columns
    cases_by_sex['women_percent'] = cases_by_sex \
        .apply(lambda x: re.sub('[()]', '', x['women'].split(' ')[1]) + '%', axis=1)
    cases_by_sex['men_percent'] = cases_by_sex \
        .apply(lambda x: re.sub('[()]', '', x['men'].split(' ')[1]) + '%', axis=1)

    # Remove the percent parentheses in women and men columns
    cases_by_sex['women'] = cases_by_sex.apply(lambda x: x['women'].split(' ')[0], axis=1).astype(int)
    cases_by_sex['men'] = cases_by_sex.apply(lambda x: x['men'].split(' ')[0], axis=1).astype(int)

    return cases_by_sex


def daily_infected():
    # Open the time series of cases for the municipalities
    municipality_cases = 'Municipality_cases_time_series.csv'

    cases_data = archive.open(municipality_cases)
    cases_df = pd.read_csv(cases_data, sep=';')

    total_daily = cases_df.groupby('date_sample').sum().sum(axis=1).values
    cases_df['total_daily'] = total_daily

    return cases_df


def geojson_convert_multipolygon(geojson_path, save_path):

    # Open the geojson that hasn't been transformed to support multipolygons
    with open(geojson_path, encoding='utf-8') as json_file:
        old_json = json.load(json_file)

    # Create a new JSON by looking at what the old includes.
    new_json = {
        'type': old_json['type'],
        'crs': old_json['crs'],
        'features': []
    }

    # Load the information csv that has been created and get the municipalities.
    info_df = pd.read_csv('data/dk-municipalities-info.csv', sep=',', index_col=0)
    municipalities = info_df.municipality.values

    # Loop through each municipality
    for muni in municipalities:
        # Set a flag that indicate if the municipality have been found
        found = False  # first time
        multi = False  # more than once

        # Going through all features in the old geojson
        for feat in old_json['features']:

            # If a municipality is found for the first time
            if not found and muni == feat['properties']['KOMNAVN']:

                # Add the feature for the municipality
                new_json['features'].append({'type': "Feature",
                                             'properties': {'REGIONKODE': feat['properties']['REGIONKODE'],
                                                            'REGIONNAVN': feat['properties']['REGIONNAVN'],
                                                            'KOMKODE': feat['properties']['KOMKODE'],
                                                            'KOMNAVN': feat['properties']['KOMNAVN']},
                                             'geometry': {'type': 'Polygon',
                                                          'coordinates': []}
                                             })
                # And add the geometry
                new_json['features'][-1]['geometry']['coordinates'] = feat['geometry']['coordinates']
                found = True  # Update flag to true

            # If municipality is found
            elif found and muni == feat['properties']['KOMNAVN']:
                # If it is the second time it is found
                if not multi:
                    # Change the geometry type to multipolygon
                    new_json['features'][-1]['geometry']['type'] = 'MultiPolygon'

                    # Get the current coordinates and make a list around them
                    current = new_json['features'][-1]['geometry']['coordinates']
                    new_json['features'][-1]['geometry']['coordinates'] = [current]

                    # Append the addiontal coordinates to this list
                    new_json['features'][-1]['geometry']['coordinates'].append(feat['geometry']['coordinates'])
                    multi = True  # Update flag
                # If found more than twice
                elif multi:
                    # Append the new coordinates
                    new_json['features'][-1]['geometry']['coordinates'].append(feat['geometry']['coordinates'])

        # If the municipality is never found, print its name for debugging
        if not found:
            print(f'The municipality {muni} wasn\'t found in the geojson')

    # Save the new geojson
    with open(save_path, 'w') as outfile:
        json.dump(new_json, outfile, indent=4)


# geojson_convert_multipolygon('data/mapsGeoJSON/dagi-500-kommuner.geojson', 'data/mapsGeoJSON/multipoly-kommuner.geojson')
