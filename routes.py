# -*- coding: utf-8 -*-
"""Routes for the menbib addon.
"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from . import views

settings_routes = {
    'rules': [
        ##### User Settings #####
        Rule(
            '/settings/menbib/',
            'get',
            views.menbib_user_config_get,
            json_renderer,
        ),

        ##### OAuth #####
        Rule(
            '/settings/menbib/oauth/',
            'get',
            views.menbib_oauth_start,  # Use same view func as node oauth start
            json_renderer,
            endpoint_suffix='_user'          # but add a suffix for url_for
        ),

        Rule(
            '/addons/menbib/oauth/finish/',
            'get',
            views.menbib_oauth_finish,
            json_renderer,
        ),

        Rule(
            '/settings/menbib/oauth/',
            'delete',
            views.menbib_oauth_delete_user,
            json_renderer,
        ),

        Rule(
            [
                '/project/<pid>/menbib/oauth/',
                '/project/<pid>/node/<nid>/menbib/oauth/',
            ],
            'get',
            views.menbib_oauth_start,
            json_renderer,
        ),
    ],
    'prefix': '/api/v1'
}



# JSON endpoints
api_routes = {
    'rules': [

        ##### Node settings #####

        Rule(
            ['/project/<pid>/menbib/config/',
            '/project/<pid>/node/<nid>/menbib/config/'],
            'get',
            views.menbib_config_get,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/menbib/config/',
            '/project/<pid>/node/<nid>/menbib/config/'],
            'put',
            views.menbib_config_put,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/menbib/config/',
            '/project/<pid>/node/<nid>/menbib/config/'],
            'delete',
            views.menbib_deauthorize,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/menbib/config/import-auth/',
            '/project/<pid>/node/<nid>/menbib/config/import-auth/'],
            'put',
            views.menbib_import_user_auth,
            json_renderer
        ),

           ##### HGrid #####
        Rule(
            [
                '/project/<pid>/menbib/hgrid/',
                '/project/<pid>/node/<nid>/menbib/hgrid/',
                '/project/<pid>/menbib/hgrid/<path:path>',
                '/project/<pid>/node/<nid>/menbib/hgrid/<path:path>',
            ],
            'get',
            views.menbib_hgrid_data_contents,
            json_renderer
        ),
    ],


    'prefix': '/api/v1'
}