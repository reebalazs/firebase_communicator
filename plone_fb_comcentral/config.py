
# Copyright (c) 2013 Enfold Systems, Inc. All rights reserved.

import os

from zope.component import queryUtility
from Products.CMFCore.interfaces import IPropertiesTool


def get_properties():
    ptool = queryUtility(IPropertiesTool)
    if ptool is not None:
        return getattr(ptool, 'firebase_comcentral_properties', None)


def get_env_config():
    """Get the configuration

    Data comes from the PLONE_MESSAGING_XXX environment variables.
    """
    return {
        'firebase_url': os.getenv('PLONE_MESSAGING_URL', ''),
        'firebase_secret': os.getenv('PLONE_MESSAGING_SECRET', ''),
        'server_id': os.getenv('PLONE_SERVER_ID', ''),
    }


def get_config():
    """Get the configuration

    Data comes from the plone site properties.

    If a given property is not found, then an
    environment variable is sourced.

    """
    props = get_properties()
    if props is not None:
        config = {
            'firebase_url': props.getProperty('firebase_url', ''),
            'firebase_secret': props.getProperty('firebase_secret', ''),
            'server_id': props.getProperty('server_id', ''),
        }
    else:
        config = {
            'firebase_url': '',
            'firebase_secret': '',
            'server_id': '',
        }
    for key, value in get_env_config().iteritems():
        if not config[key]:
            config[key] = value
    # server id must have some default
    if config['server_id'] == '':
        config['server_id'] = 'plone'
    return config
