#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import json
import os
from os.path import dirname, abspath, join as pathjoin

METADATA_ROOT = abspath(pathjoin(abspath(dirname(__file__)), '..', 'static', 'images', 'metadata'))
IMAGES_ROOT = abspath(pathjoin(abspath(dirname(__file__)), '..', 'static', 'images', 'scaled'))


current_index = None
images = None


def write_current_index():
    if images is not None:
        with open(pathjoin(METADATA_ROOT, current_index + '_images.json'), 'w') as jsonfile:
            json.dump({'images': images}, jsonfile)


for _, _, filenames in os.walk(IMAGES_ROOT):
    for filename in sorted(filenames):
        if filename.endswith('.JPG'):
            index = filename[:8]
            if index != current_index:
                # Write image index if we have one
                write_current_index()
                # Start a new index
                images = []
                current_index = index

            images.append(filename)

    write_current_index()
