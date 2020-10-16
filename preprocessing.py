import json
import pandas as pd


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
