import json

# ==============================
# == Expo Line

with open('expo-line.geojson') as jfile:
    expo = json.load(jfile)

expo_share_ids = [12,13,14]
expo_reverse_ids = list(range(20,29)) + [200,210,211,220,240,241,250,251,260]

for f in expo['features']:
    # Delete extra properties
    del f['properties']['NAME']
    del f['properties']['PHASE']
    del f['properties']['Lenth']
    del f['properties']['Miles']

    # Reverse mis-directed segments
    if f['properties']['ID'] in expo_reverse_ids:
        f['geometry']['coordinates'] = f['geometry']['coordinates'][::-1]

    # Mark portions of the line that are shared
    # with the Blue line
    if f['properties']['ID'] in expo_share_ids:
        f['properties']['shared'] = True
    else:
        f['properties']['shared'] = False

with open('expo-line.geojson', 'w') as jfile:
    json.dump(expo, jfile)


# ==============================
# == Blue Line

with open('blue-line.geojson') as jfile:
    blue = json.load(jfile)

for f in blue['features']:
    # Mark portions of the line that are shared
    # with the Blue line
    if 33 < f['properties']['bearing'] < 43:
        f['properties']['shared'] = True
    else:
        f['properties']['shared'] = False

    # Delete extra properties
    del f['properties']['PATH_ID']
    del f['properties']['LINE']
    del f['properties']['Miles']
    del f['properties']['Feet']

with open('blue-line.geojson', 'w') as jfile:
    json.dump(blue, jfile)
