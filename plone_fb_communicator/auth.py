
# Copyright (c) 2013 Enfold Systems, Inc. All rights reserved.

from firebase_token_generator import create_token
from zope.component import getMultiAdapter
from Products.Five import BrowserView

from .config import (
    get_config,
)


def get_user_data(context, request):
    """Return a {'user_id':..., 'full_name': ..., portrait_url: ...} dictionary
    user_id is None (if anon),

    or (XXX currently disabled) False,
    if the user is not allowed to use this feature.
    """
    portal_state = getMultiAdapter((context, request), name="plone_portal_state")
    member = portal_state.member()
    user_id = member.getId()
    full_name = member.getProperty('fullname')
    try:
        method = member.getPersonalPortrait
    except AttributeError:
        # default portrait: return empty string, meaning no portrait.
        portrait_url = ''
    else:
        member_image = method()
        portrait_url = member_image.absolute_url()
        if portrait_url.endswith('/defaultUser.png'):
            # default portrait: return empty string, meaning no portrait.
            portrait_url = ''

    # XXX TODO set this based on permission
    is_admin = user_id == 'admin'

    return dict(
        user_id=user_id,
        full_name=full_name,
        portrait_url=portrait_url,
        is_admin=is_admin,
    )

    # XXX XXX filter_users is currently not used.
    #
    ## If the user is not allowed, refuse to give a token.
    #props = get_properties()
    #
    #if props is not None and \
    #        props.getProperty('filter_users', False) and \
    #        user_id not in props.getProperty('allowed_users', ()):
    #    # User is not allowed.
    #    return False
    #else:
    #    return user_id


def get_allowed_userid(context, request):
    return get_user_data(context, request)['user_id']


def get_auth_info(context, request, force_admin=False):
    if not force_admin:
        user_data = get_user_data(context, request)
    else:
        user_data = dict(
            user_id='admin',
            full_name='',
            portrait_url='',
            is_admin=True,
        )

    config = get_config()

    custom_data = {
        'server_id': config['server_id'],
        'user_id': user_data['user_id'],
        'full_name': user_data['full_name'],
        'portrait_url': user_data['portrait_url'],
        'is_admin': user_data['is_admin'],
    }
    options = {
        'admin': user_data['is_admin'],
    }

    if user_data['user_id'] is not None and user_data['user_id'] is not False:
        token = create_token(config['firebase_secret'], custom_data, options)
    else:
        # If the user is not allowed, (user_id is None) return a void token.
        # If the user is anonymous (not logged in), (user_id is False) we do not
        # allow it either. Return a void token.
        token = ''

    # Some info that is not auth related
    portal_state = getMultiAdapter((context, request), name="plone_portal_state")
    portal_url = portal_state.portal_url()
    static = {
        'root':  portal_url + '/++resource++fb_communicator/',
    }

    return dict(
        auth_token=token,
        auth_data=custom_data,
        config=config,
        static=static,
    )


def get_auth_token(context, request, force_admin=False):
    get_auth_info(context, request, force_admin=False)['auth_token']


class AllowedUseridView(BrowserView):

    def __call__(self):
        return get_allowed_userid(self.context, self.request)
