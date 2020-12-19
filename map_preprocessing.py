import json
import pandas as pd


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


geojson_convert_multipolygon('data/mapsGeoJSON/dagi-500-kommuner.geojson',
                             'data/mapsGeoJSON/multipoly-kommuner.geojson')
