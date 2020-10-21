import json
import zipfile as zp
import re
import pandas as pd

archive = zp.ZipFile('Data-Epidemiologiske-Rapport-08102020-da23.zip', 'r')




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


def geojson_convert_multipolygon(geojson_path, save_path):
    with open(geojson_path, encoding='utf-8') as json_file:
        old_json = json.load(json_file)

    new_json = {
        'type': old_json['type'],
        'crs': old_json['crs'],
        'features': []
    }

    info_df = pd.read_csv('dk-municipalities-info.csv', sep=',', index_col=0)
    municipalities = info_df.municipality.values

    for muni in municipalities:
        found = False
        multi = False
        for feat in old_json['features']:
            if not found and muni == feat['properties']['KOMNAVN']:

                new_json['features'].append({'type': "Feature",
                                             'properties': {'REGIONKODE': feat['properties']['REGIONKODE'],
                                                            'REGIONNAVN': feat['properties']['REGIONNAVN'],
                                                            'KOMKODE': feat['properties']['KOMKODE'],
                                                            'KOMNAVN': feat['properties']['KOMNAVN']},
                                             'geometry': {'type': 'Polygon',
                                                          'coordinates': []}
                                             })
                new_json['features'][-1]['geometry']['coordinates'] = feat['geometry']['coordinates']
                found = True

            elif found and muni == feat['properties']['KOMNAVN']:
                if not multi:
                    new_json['features'][-1]['geometry']['type'] = 'MultiPolygon'
                    current = new_json['features'][-1]['geometry']['coordinates']
                    new_json['features'][-1]['geometry']['coordinates'] = [current]
                    new_json['features'][-1]['geometry']['coordinates'].append(feat['geometry']['coordinates'])
                    multi = True
                elif multi:
                    new_json['features'][-1]['geometry']['coordinates'].append(feat['geometry']['coordinates'])

        if not found:
            print(f'The municipality {muni} wasn\'t found in the geojson')

    with open(save_path, 'w') as outfile:
        json.dump(new_json, outfile, indent=4)


# geojson_convert_multipolygon('mapsGeoJSON/dagi-500-kommuner.geojson', 'mapsGeoJSON/multipoly-kommuner.geojson')
