# -*- coding: utf-8 -*-
"""Utility functions for the MendeleyBibliography add-on.
"""

def serialize_urls(node_settings):
    node = node_settings.owner
    urls = {
        'config': node.api_url_for('menbib_config_put'),
        'deauthorize': node.api_url_for('menbib_deauthorize'),
        'auth': node.api_url_for('menbib_oauth_start'),
        'importAuth': node.api_url_for('menbib_import_user_auth')
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
        result['urls']['owner'] = web_url_for('profile_view_id',
                                               uid=user_settings.owner._primary_key)
        result['ownerName'] = user_settings.owner.fullname
    return rv
