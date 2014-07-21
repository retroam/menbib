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


def folder_to_hgrid(item, node, permissions):
    """Serializes folder names (returned from Mendeley)
    to the format expected by Rubeus/HGrid.
    """
    serialized = {
        'addon': 'menbib',
        'permissions': permissions,
        'name': item,
        rubeus.KIND: rubeus.FOLDER,
        'urls': node.api_url_for('menbib_hgrid_data_contents'),
    }
    return serialized