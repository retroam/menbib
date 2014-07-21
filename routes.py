# -*- coding: utf-8 -*-
"""Routes for the menbib addon.
"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer
from website.addons.menbib import views


settings_routes = {
    'rules': [
        ##### User Settings #####
        Rule(
            '/settings/menbib/',
            'get',
            views.auth.menbib_user_config_get,
            json_renderer,
        ),

        ##### OAuth #####
        Rule(
            '/settings/menbib/oauth/',
            'get',
            views.auth.menbib_oauth_start,  # Use same view func as node oauth start
            json_renderer,
            endpoint_suffix='_user'          # but add a suffix for url_for
        ),

        Rule(
            '/addons/menbib/oauth/finish/',
            'get',
            views.auth.menbib_oauth_finish,
            json_renderer,
        ),

        Rule(
            '/settings/menbib/oauth/',
            'delete',
            views.auth.menbib_oauth_delete_user,
            json_renderer,
        ),

        Rule(
            [
                '/project/<pid>/menbib/oauth/',
                '/project/<pid>/node/<nid>/menbib/oauth/',
            ],
            'get',
            views.auth.menbib_oauth_start,
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
            views.auth.menbib_config_get,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/menbib/config/',
            '/project/<pid>/node/<nid>/menbib/config/'],
            'put',
            views.auth.menbib_config_put,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/menbib/config/',
            '/project/<pid>/node/<nid>/menbib/config/'],
            'delete',
            views.auth.menbib_deauthorize,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/menbib/config/import-auth/',
            '/project/<pid>/node/<nid>/menbib/config/import-auth/'],
            'put',
            views.auth.menbib_import_user_auth,
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
            views.hgrid.menbib_hgrid_data_contents,
            json_renderer
        ),


    ],


    'prefix': '/api/v1'
}

page_routes = {
    'rules': [
        ##### Page #####
    Rule(
        [
            '/<pid>/menbib',
            '/project/<pid>/menbib/page/',
            '/project/<pid>/node/<nid>/menbib/page/',
            '/project/<pid>/menbib/page/<path:path>',
            '/project/<pid>/node/<nid>/menbib/page/<path:path>',
        ],
        'get',
        views.page.menbib_get_page_info,
        OsfWebRenderer('../addons/menbib/templates/menbib_page.mako')
        ),
    Rule(
        [
            '/project/<pid>/menbib/getExport/',
            '/project/<pid>/node/<nid>/menbib/getExport/',
            '/project/<pid>/menbib/getExport/<path:path>',
            '/project/<pid>/node/<nid>/menbib/getExport/<path:path>',
        ],
        'get',
        views.page.menbib_get_export,
        OsfWebRenderer('../addons/menbib/templates/menbib_page.mako')
        ),
    Rule(
        [
            '/project/<pid>/menbib/getCitation/',
            '/project/<pid>/node/<nid>/menbib/getCitation/',
            '/project/<pid>/menbib/page/<path:path>',
            '/project/<pid>/node/<nid>/menbib/getCitation/<path:path>',
        ],
        'get',
        views.page.menbib_get_citation,
        OsfWebRenderer('../addons/menbib/templates/menbib_page.mako')
        ),
        ]
}