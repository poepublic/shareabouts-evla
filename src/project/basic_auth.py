from __future__ import unicode_literals

import base64
import os

import logging
log = logging.getLogger(__name__)

def BasicAuthMiddleware(application):
    username = os.environ.get('BASIC_AUTH_USERNAME')
    password = os.environ.get('BASIC_AUTH_PASSWORD')
    is_protected = (username and password)

    def not_authorized(environ, start_response, msg=None):
        start_response('401 NOT AUTHORIZED', [('WWW-Authenticate', 'Basic')])
        if msg:
            log.warn('Not authorized: ' + msg)
        yield (msg or b'Not Authorized')

    def protected_application(environ, start_response):
        auth = environ.get('HTTP_AUTHORIZATION', b'').split()
        is_path_exempt = False

        # Check if the auth cookie is already around
        if environ['PATH_INFO'].startswith('/api'):
            del environ['HTTP_AUTHORIZATION']
            is_path_exempt = True

        if not is_path_exempt:
            if not auth or auth[0].lower() != b'basic':
                return not_authorized(environ, start_response)

            if len(auth) == 1:
                return not_authorized(environ, start_response, 'Invalid basic header. No credentials provided.')

            if len(auth) > 2:
                return not_authorized(environ, start_response, 'Invalid basic header. Credentials string should not contain spaces.')

            try:
                auth_parts = base64.b64decode(auth[1]).decode('iso-8859-1').partition(':')
            except (TypeError, UnicodeDecodeError):
                return not_authorized(environ, start_response, 'Invalid basic header. Credentials not correctly base64 encoded.')

            if (username, password) != (auth_parts[0], auth_parts[2]):
                return not_authorized(environ, start_response, 'Invalid username/password.')

        return application(environ, start_response)

    return protected_application if is_protected else application
