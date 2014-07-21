# -*- coding: utf-8 -*-
from webtest_plus import TestApp
from nose.tools import *  # PEP8 asserts
import mock
from tests.base import OsfTestCase, URLLookup, assert_is_redirect
from tests.factories import AuthUserFactory, ProjectFactory
from website.util import api_url_for, web_url_for
from collections import namedtuple

from .utils import app, MenbibAddonTestCase, patch_client, MockMenbib
from factories import MenbibNodeSettingsFactory


mock_client = MockMenbib()

lookup = URLLookup(app)
AuthResult = namedtuple('AuthResult',
                        ['access_token', 'refresh_token',
                         'token_type', 'expires_in'])

class TestMenbibAuthViews(OsfTestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.app.authenticate(*self.user.auth)

    def test_menbib_oauth_start(self):
        url = api_url_for('menbib_oauth_start_user')
        res = self.app.get(url)
        assert_is_redirect(res)

    @mock.patch('website.addons.menbib.views.auth.finish_auth')
    def test_menbib_oauth_finish(self, mock_finish):
        mock_finish.return_value = AuthResult('mytokenabc', 'myrefreshabc', 'cool', '3600')
        url = api_url_for('menbib_oauth_finish')
        res = self.app.get(url)
        assert_is_redirect(res)

    def test_menbib_oauth_delete_user(self):
        self.user.add_addon('menbib')
        user_settings = self.user.get_addon('menbib')
        user_settings.access_token = '12345abc'
        assert_true(user_settings.has_auth)
        self.user.save()
        url = api_url_for('menbib_oauth_delete_user')
        res = self.app.delete(url)
        user_settings.reload()
        assert_false(user_settings.has_auth)


class TestFolderViews(MenbibAddonTestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.app.authenticate(*self.user.auth)
        self.user_settings = self.user.get_addon('menbib')
        self.node_settings = MenbibNodeSettingsFactory(
            user_settings=self.user_settings)
        self.project = self.node_settings.owner

    # def test_menbib_hgrid_data_contents_if_folder_is_none(self):
    #     # If folder is set to none, no data are returned
    #     print self.node_settings.folder
    #     self.node_settings.folder = None
    #     self.node_settings.save()
    #     print self.node_settings.folder
    #     url = api_url_for('menbib_hgrid_data_contents', pid=self.project._primary_key)
    #     res = self.app.get(url, auth=self.user.auth)
    #     print res.json()
    #     # assert_equal(res.json['data'], [])

    # def test_menbib_hgrid_data_contents(self):
    #     with patch_client('website.addons.menbib.views.get_node_client'):
    #         print self.node_settings.folder
    #         url = api_url_for('menbib_hgrid_data_contents',
    #                             pid=self.project._primary_key)
    #         print url
    #         res = self.app.get(url, auth=self.user.auth)
    #         # folders = mock_client.folders()
    #         # print res.json()
    #         # print folders




class TestPageViews(MenbibAddonTestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.app.authenticate(*self.user.auth)
        self.user_settings = self.user.get_addon('menbib')
        self.node_settings = MenbibNodeSettingsFactory(
        user_settings=self.user_settings)
        self.project = self.node_settings.owner

    def test_menbib_page(self):
        url = web_url_for('menbib_get_page_info', pid=self.project._primary_key)
        print url
        res = self.app.get(url, auth=self.user.auth)

    def test_mendeley_export(self):
        pass

    def test_mendeley_citation(self):
        pass