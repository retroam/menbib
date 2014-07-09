# -*- coding: utf-8 -*-
"""Routes for the menbib addon.
"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from . import views

# Routes that use the web renderer
web_routes = {
    'rules': [

        ##### View file #####
    #     Rule(
    #         [
    #             '/project/<pid>/menbib/files/<path:path>',
    #             '/project/<pid>/node/<nid>/menbib/files/<path:path>',
    #         ],
    #         'get',
    #         views.crud.menbib_view_file,
    #         OsfWebRenderer('../addons/menbib/templates/menbib_view_file.mako'),
    #     ),


    #     ##### Download file #####
    #     Rule(
    #         [
    #             '/project/<pid>/menbib/files/<path:path>/download/',
    #             '/project/<pid>/node/<nid>/menbib/files/<path:path>/download/',
    #         ],
    #         'get',
    #         views.crud.menbib_download,
    #         notemplate,
    #     ),
    ],
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
    ],

    ## Your routes here

    'prefix': '/api/v1'
}