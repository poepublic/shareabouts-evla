"""
Before you run this script, you should have two files:

* potential-sites.geojson: A geojson representation of each potential site.
"""

from __future__ import print_function, unicode_literals

import json
import csv
import requests
import sys
import os
import re
from os.path import dirname, abspath, join as pathjoin

DATA_ROOT = abspath(pathjoin(abspath(dirname(__file__)), '..', 'data'))

with open(pathjoin(DATA_ROOT, 'potential-sites.geojson')) as jfile:
    data = json.load(jfile)

with open(pathjoin(DATA_ROOT, 'site-metadata.csv'), 'rU') as cfile:
    reader = csv.DictReader(cfile)
    metadata_list = list(reader)

metadata = {}
for m in metadata_list:
    sid = m['New Location'] + m['Site']
    print(sid)
    metadata[sid] = m

for f in data['features']:
    # Get rid of extra, uneccessary properties in the geojson
    keep_props = ('Site_ID', 'Name')
    for prop in f['properties'].keys():
        if prop not in keep_props:
            del f['properties'][prop]

    sid = f['properties'].pop('Name')
    if sid in metadata:
        m = metadata[sid]
        f['properties']['Site_ID'] = sid.zfill(5)
    else:
        for sitetype in 'ABCDEF':
            if (sid + sitetype) in metadata:
                m = metadata[sid + sitetype]
                f['properties']['Site_ID'] = sid.zfill(4) + sitetype
                break
        else:
            print(sid + ' not in metadata')
    f['properties']['location_name'] = m['Name']
    f['properties']['location_type'] = 'specific'
    f['properties']['Streetview Link'] = m['Streetview Link']
    f['properties']['Street'] = m['Street']
    f['properties']['Cross Street 1'] = m['Cross Street 1']
    f['properties']['Cross Street 2'] = m['Cross Street 2']
    f['properties']['Comments'] = m['Comments']
    f['properties']['submitter'] = None

    if f['properties']['Streetview Link'] == 'Show at the intersection':
        del f['properties']['Streetview Link']
        f['properties']['location_type'] = 'intersection'

    elif f['properties']['Streetview Link'] == 'Show at general location':
        del f['properties']['Streetview Link']
        f['properties']['location_type'] = 'general'

    else:
        match = re.match(
            r'^https://www.google.com/maps/@([\d\.-]+,[\d\.-]+),.*,([\d\.-]+)h,.*',
            f['properties']['Streetview Link'],
        )
        assert match, (
            'The location ' + sid + ' has an unexpected Streetview link of "' +
            f['properties']['Streetview Link'] + '".'
        )
        f['properties']['Streetview Image'] = 'https://maps.googleapis.com/maps/api/streetview?size=800x400&location={}&heading={}'.format(match.group(1), match.group(2))

# with open('updated-potential-sites.geojson', 'w') as jfile:
#     json.dump(data, jfile)

try:
    key = sys.argv[1]
except IndexError:
    key = os.environ['SHAREABOUTS_DATASET_KEY']

print('Key is ' + key)

for new_place_data in data['features']:
    if 'Site_ID' not in new_place_data['properties']:
        continue

    sid = new_place_data['properties']['Site_ID']
    res = requests.get(
        'https://shareaboutsapi2.herokuapp.com/api/v2/toole/datasets/bikesharela/places?Site_ID=' + sid,
        headers={'Content-type': 'application/json'}
    )
    old_places = res.json()
    if old_places['features']:
        print('Updating...', end='')
        old_place = old_places['features'][0]
        url = old_place['properties']['url']
        request_method = requests.patch
    else:
        print('Creating...', end='')
        url = 'https://shareaboutsapi2.herokuapp.com/api/v2/toole/datasets/bikesharela/places'
        request_method = requests.post

    res = request_method(
        url,
        data=json.dumps(new_place_data),
        headers={
            'Content-type': 'application/json',
            'X-Shareabouts-Silent': 'True',
            'X-Shareabouts-Key': key
        }
    )
    print(res)
