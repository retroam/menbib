# -*- coding: utf-8 -*-
from framework import request
from framework.auth import get_current_user
from website.project.decorators import (must_be_valid_project,
    must_have_addon, must_have_permission, must_not_be_registration
)
from .utils import serialize_settings
from framework.auth.decorators import must_be_logged_in
from website.util import api_url_for, web_url_for
import httplib as http
from framework.sessions import session
from framework import redirect, request
from framework.exceptions import HTTPError
from framework.status import push_status_message as flash
from requests_oauthlib import OAuth2Session
from . import settings as menbib_settings


def get_auth_flow():
    redirect_uri = api_url_for('menbib_oauth_finish', _absolute=True)
    return OAuth2Session(
        menbib_settings.CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=menbib_settings.SCOPE,
    )


def menbib_oauth_start(**kwargs):
    user = get_current_user()
    nid = kwargs.get('pid') or kwargs.get('nid')
    if nid:
        session.data['menbib_auth_nid'] = nid
    if not user:
        raise HTTPError(http.FORBIDDEN)
    if user.has_addon('menbib') and user.get_addon('menbib').has_auth:
        flash('You have already authorized Mendeley for this account', 'warning')
        return redirect(web_url_for('user_addons'))
    return redirect(get_auth_flow())



def menbib_oauth_finish():
    return {}


def menbib_oauth_delete_user():
    return {}

@must_be_valid_project
@must_have_addon('menbib', 'node')
def menbib_config_get(node_addon, **kwargs):
    """API that returns the serialized node settings."""
    user = get_current_user()
    return {
        'result': serialize_settings(node_addon, user),
    }, http.OK

    
@must_have_permission('write')
@must_not_be_registration
@must_have_addon('menbib', 'node')
def menbib_config_put(node_addon, auth, **kwargs):
    """View for changing a node's linked Mendeley folder."""
    folder = request.json.get('selected')
    path = folder['path']
    node_addon.set_folder(path, auth=auth)
    node_addon.save()
    return {
        'result': {
            'folder': {
                'name': 'Menbib' + path,
                'path': path
            },
            'urls': serialize_urls(node_addon)
        },
        'message': 'Successfully updated settings.',
    }, http.OK


@must_have_permission('write')
@must_have_addon('menbib', 'node')
def menbib_deauthorize(auth, node_addon, **kwargs):
    node_addon.deauthorize(auth=auth)
    node_addon.save()
    return None


@must_have_permission('write')
@must_have_addon('menbib', 'node')
def menbib_import_user_auth(auth, node_addon, **kwargs):
    """Import menbib credentials from the currently logged-in user to a node.
    """
    user = auth.user
    user_addon = user.get_addon('menbib')
    if user_addon is None or node_addon is None:
        raise HTTPError(http.BAD_REQUEST)
    node_addon.set_user_auth(user_addon)
    node_addon.save()
    return {
        'result': serialize_settings(node_addon, user),
        'message': 'Successfully imported access token from profile.',
    }, http.OK

@must_be_logged_in
@must_have_addon('menbib', 'user')
def menbib_user_config_get(user_addon, auth, **kwargs):
    """View for getting a JSON representation of the logged-in user's
    Mendeley user settings.
    """
    urls = {
        'create': api_url_for('menbib_oauth_start_user'),
        'delete': api_url_for('menbib_oauth_delete_user')
    }
    info = user_addon.menbib_info

    return {
        'result': {
            'userHasAuth': user_addon.has_auth,
            'menbibName': info['display_name'] if info else None,
            'urls': urls,
        },
    }, http.OK
