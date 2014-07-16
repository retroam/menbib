# -*- coding: utf-8 -*-
"""Utility functions for the MendeleyBibliography add-on.
"""
from website.util import web_url_for
import os
from website.util import rubeus
from framework.exceptions import HTTPError
import httplib as http

def serialize_urls(node_settings):
    node = node_settings.owner
    urls = {
        'config': node.api_url_for('menbib_config_put'),
        'deauthorize': node.api_url_for('menbib_deauthorize'),
        'auth': node.api_url_for('menbib_oauth_start'),
        'importAuth': node.api_url_for('menbib_import_user_auth'),
        'folders': node.api_url_for('menbib_hgrid_data_contents')
    }
    return urls


def serialize_settings(node_settings, current_user):
    """
    View helper that returns a dictionary representation of a MenbibNodeSettings record. Provides the return value for the menbib config endpoints.
    """
    user_settings = node_settings.user_settings
    user_is_owner = user_settings is not None and (
        user_settings.owner._primary_key == current_user._primary_key
    )
    current_user_settings = current_user.get_addon('menbib')
    rv = {
        'nodeHasAuth': node_settings.has_auth,
        'userIsOwner': user_is_owner,
        'userHasAuth': current_user_settings is not None and current_user_settings.has_auth,
        'urls': serialize_urls(node_settings)
    }
    if node_settings.has_auth:
    # Add owner's profile URL
        rv['urls']['owner'] = web_url_for('profile_view_id',
                                               uid=user_settings.owner._primary_key)
        rv['ownerName'] = user_settings.owner.fullname
        path = node_settings.folder
        if path is None:
            rv['folder'] = {'name': None, 'path': None}
        else:
            rv['folder'] = {
                'name': 'Menbib' + path,
                'path': path
            }
    return rv


def is_authorizer(auth, node_addon):
    """Return if the auth object's user is the same as the authorizer of the node."""
    return auth.user == node_addon.user_settings.owner


def clean_path(path):
    """Ensure a path is formatted correctly for url_for."""
    if path is None:
        return ''
    return path.strip('/')


def is_subdir(path, directory):
    if not (path and directory):
        return False
    #make both absolute
    abs_directory = os.path.abspath(directory)
    abs_path = os.path.abspath(path)
    return os.path.commonprefix([abs_path, abs_directory]) == abs_directory


def abort_if_not_subdir(path, directory):
    """Check if path is a subdirectory of directory. If not, abort the current
    request with a 403 error.
    """
    if not is_subdir(clean_path(path), clean_path(directory)):
        raise HTTPError(http.FORBIDDEN)
    return True


def get_file_name(path):
    """Given a path, get just the base filename.
    Handles "/foo/bar/baz.txt/" -> "baz.txt"
    """
    return os.path.basename(path.strip('/'))


def build_menbib_urls(item, node):
    if item['is_dir']:
        return {
            'folders': node.api_url_for('menbib_hgrid_data_contents')
        }


def metadata_to_hgrid(item, node, permissions):
    """Serializes a dictionary of metadata (returned from Mendeley)
    to the format expected by Rubeus/HGrid.
    """
    filename = get_file_name(item['path'])
    serialized = {
        'addon': 'menbib',
        'permissions': permissions,
        'name': get_file_name(item['path']),
        'ext': os.path.splitext(filename)[1],
        rubeus.KIND: rubeus.FOLDER if item['is_dir'] else rubeus.FILE,
        'urls': build_menbib_urls(item, node),
        'path': item['path'],
    }
    return serialized