#!/usr/bin/env python3

import csv
import os
import requests
import sys


def get_with_retry(url, *args, retries=10, **kwargs):
    """ Request with GET until successful. """
    while retries > 0:
        retries -= 1
        print('Trying to retrieve {}'.format(url), file=sys.stderr)
        response = requests.get(url, *args, **kwargs)
        if response.status_code == 200:
            return response
        else:
            print('Failed {}: {}'.format(response.status_code, response.content), file=sys.stderr)


def get_all_pages(starturl, apikey, resultskey='results'):
    """ Page through multi-page list of data. """
    nexturl = starturl
    data = []
    while nexturl:
        response = get_with_retry(nexturl, headers={'x-shareabouts-key': apikey})
        pagedata = response.json()
        data.extend(pagedata[resultskey])
        nexturl = pagedata['metadata']['next']
    return data


def get_locations(apiroot, apikey):
    features = get_all_pages(apiroot + '/places?include_private', apikey, resultskey='features')
    locations = {}
    for feature in features:
        props = feature['properties']
        props['id'] = feature['id']

        if 'station' in props:
            props['approx_address'] = props['station']['street']
            props.pop('station')

        if 'private-why_good' in props:
            props['surveys'] = [props]
        else:
            props['surveys'] = []

        locations[props['url']] = {
            'geometry': feature['geometry'],
            **props,
        }
    return locations


def get_surveys(apiroot, apikey):
    locations = get_locations(apiroot, apikey)
    surveys = get_all_pages(apiroot + '/surveys?include_private', apikey)

    for survey in surveys:
        location_url = survey.pop('place')
        location = locations[location_url]
        location['surveys'].append(survey)
    return locations


def output_surveys(locations_w_surveys):
    writer = csv.writer(sys.stdout)
    writer.writerow([
        'Location ID',
        'Location Name',
        'Approx Address',
        'Lat',
        'Lon',
        'Good Spot?',
        'Good Spot Reason',
        'Good Spot Other Reason',
        'Bad Spot Reason',
        'Bad Spot Other Reason',
        'Other Info About Spot',
        'Business/Property Owner?',
        'Business Name',
        'Business Address',
        'Business Contact',
        'Age Group',
        'Race(s)',
        'Income Range',
        'Vehicles in Household',
        'Email Address',
    ])

    for location_id, location in locations_w_surveys.items():
        surveys = location['surveys']
        for survey in surveys:
            writer.writerow([
                location['id'],
                location.get('location_name'),
                location.get('approx_address'),
                location['geometry']['coordinates'][1],
                location['geometry']['coordinates'][0],
                survey.get('private-good_spot', 'yes'),
                survey.get('private-why_good', ''),
                survey.get('private-why_good_other_reason', ''),
                survey.get('private-why_bad', ''),
                survey.get('private-why_bad_other_reason', ''),
                survey.get('private-other_info', ''),
                survey.get('private-owner', ''),
                survey.get('private-business_name', ''),
                survey.get('private-business_address', ''),
                survey.get('private-business_contact', ''),
                survey.get('private-submitter_age', ''),
                survey.get('private-submitter_race', ''),
                survey.get('private-submitter_income', ''),
                survey.get('private-submitter_vehicles_owned', ''),
                survey.get('private-submitter_email', ''),
            ])


if __name__ == '__main__':
    apiroot = 'https://shareaboutsapi.poepublic.com/api/v2/sumc/datasets/evla'
    apikey = os.environ['DATASET_KEY']

    surveys = get_surveys(apiroot, apikey)
    output_surveys(surveys)