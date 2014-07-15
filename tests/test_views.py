# -*- coding: utf-8 -*-
from webtest_plus import TestApp
from nose.tools import *  # PEP8 asserts
import mock
from tests.base import OsfTestCase, URLLookup, assert_is_redirect
from tests.factories import AuthUserFactory
from website.util import api_url_for
from collections import namedtuple

from .utils import app, MenbibAddonTestCase

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

    @mock.patch('website.addons.menbib.views.finish_auth')
    def test_menbib_oauth_finish(self, mock_finish):
        mock_finish.return_value = AuthResult('mytokenabc', 'myrefreshabc', 'cool', '3600')
        url = api_url_for('menbib_oauth_finish')
        res = self.app.get(url)
        assert_is_redirect(res)

    def test_menbib_oauth_delete_user(self):
        self.user.add_addon('menbib')
        user_settings = self.user.get_addon('menbib')
        user_settings.access_token = '12345abc'
        user_settings.save()
        assert_true(user_settings.has_auth)
        self.user.save()
        url = api_url_for('menbib_oauth_delete_user')
        res = self.app.delete(url)
        user_settings.reload()
        assert_false(user_settings.has_auth)


# class TestConfigViews(MenbibAddonTestCase):
#
#     def test_dropbox_user_config_get_has_auth_info(self):
#         url = api_url_for('dropbox_user_config_get')
#         res = self.app.get(url, auth=self.user.auth)
#         assert_equal(res.status_code, 200)
#         # The JSON result
#         result = res.json['result']
#         assert_true(result['userHasAuth'])
#
#     def test_dropbox_user_config_get_returns_correct_urls(self):
#         url = api_url_for('dropbox_user_config_get')
#         res = self.app.get(url, auth=self.user.auth)
#         assert_equal(res.status_code, 200)
#         # The JSONified URLs result
#         urls = res.json['result']['urls']
#         assert_equal(urls['delete'], api_url_for('dropbox_oauth_delete_user'))
#         assert_equal(urls['create'], api_url_for('dropbox_oauth_start_user'))
#
#     def test_serialize_settings_helper_returns_correct_urls(self):
#         result = serialize_settings(self.node_settings, self.user, client=mock_client)
#         urls = result['urls']
#
#         assert_equal(urls['config'], self.project.api_url_for('dropbox_config_put'))
#         assert_equal(urls['deauthorize'], self.project.api_url_for('dropbox_deauthorize'))
#         assert_equal(urls['auth'], self.project.api_url_for('dropbox_oauth_start'))
#         assert_equal(urls['importAuth'], self.project.api_url_for('dropbox_import_user_auth'))
#         assert_equal(urls['files'], self.project.web_url_for('collect_file_trees__page'))
#         assert_equal(urls['share'], utils.get_share_folder_uri(self.node_settings.folder))
#         # Includes endpoint for fetching folders only
#         # NOTE: Querystring params are in camelCase
#         assert_equal(urls['folders'],
#             self.project.api_url_for('dropbox_hgrid_data_contents', foldersOnly=1, includeRoot=1))
#
#     def test_serialize_settings_helper_returns_correct_auth_info(self):
#         result = serialize_settings(self.node_settings, self.user, client=mock_client)
#         assert_equal(result['nodeHasAuth'], self.node_settings.has_auth)
#         assert_true(result['userHasAuth'])
#         assert_true(result['userIsOwner'])
#
#     def test_serialize_settings_for_user_no_auth(self):
#         no_addon_user = AuthUserFactory()
#         result = serialize_settings(self.node_settings, no_addon_user, client=mock_client)
#         assert_false(result['userIsOwner'])
#         assert_false(result['userHasAuth'])
#
#
#     def test_serialize_settings_helper_returns_correct_folder_info(self):
#         result = serialize_settings(self.node_settings, self.user, client=mock_client)
#         folder = result['folder']
#         assert_equal(folder['name'], 'Dropbox' + self.node_settings.folder)
#         assert_equal(folder['path'], self.node_settings.folder)
#
#     def test_dropbox_config_get(self):
#         self.user_settings.save()
#
#         url = api_url_for('dropbox_config_get', pid=self.project._primary_key)
#
#         res = self.app.get(url, auth=self.user.auth)
#         assert_equal(res.status_code, 200)
#         result = res.json['result']
#         assert_equal(result['ownerName'], self.user_settings.owner.fullname)
#
#         assert_equal(result['urls']['config'],
#             api_url_for('dropbox_config_put', pid=self.project._primary_key))
#
#     def test_dropbox_config_put(self):
#         url = api_url_for('dropbox_config_put', pid=self.project._primary_key)
#         # Can set folder through API call
#         res = self.app.put_json(url, {'selected': {'path': 'My test folder',
#             'name': 'Dropbox/My test folder'}},
#             auth=self.user.auth)
#         assert_equal(res.status_code, 200)
#         self.node_settings.reload()
#         self.project.reload()
#
#         # Folder was set
#         assert_equal(self.node_settings.folder, 'My test folder')
#         # A log event was created
#         last_log = self.project.logs[-1]
#         assert_equal(last_log.action, 'dropbox_folder_selected')
#         params = last_log.params
#         assert_equal(params['folder'], 'My test folder')
#
#     def test_dropbox_deauthorize(self):
#         url = api_url_for('dropbox_deauthorize', pid=self.project._primary_key)
#         saved_folder = self.node_settings.folder
#         self.app.delete(url, auth=self.user.auth)
#         self.project.reload()
#         self.node_settings.reload()
#
#         assert_false(self.node_settings.has_auth)
#         assert_is(self.node_settings.user_settings, None)
#         assert_is(self.node_settings.folder, None)
#
#         # A log event was saved
#         last_log = self.project.logs[-1]
#         assert_equal(last_log.action, 'dropbox_node_deauthorized')
#         log_params = last_log.params
#         assert_equal(log_params['node'], self.project._primary_key)
#         assert_equal(log_params['folder'], saved_folder)
#
#     def test_dropbox_import_user_auth_returns_serialized_settings(self):
#         # Node does not have user settings
#         self.node_settings.user_settings = None
#         self.node_settings.save()
#         url = api_url_for('dropbox_import_user_auth', pid=self.project._primary_key)
#         res = self.app.put(url, auth=self.user.auth)
#         self.project.reload()
#         self.node_settings.reload()
#         expected_result = serialize_settings(self.node_settings, self.user,
#                                              client=mock_client)
#         result = res.json['result']
#         assert_equal(result, expected_result)
#
#     def test_dropbox_import_user_auth_adds_a_log(self):
#         # Node does not have user settings
#         self.node_settings.user_settings = None
#         self.node_settings.save()
#         url = api_url_for('dropbox_import_user_auth', pid=self.project._primary_key)
#         self.app.put(url, auth=self.user.auth)
#         self.project.reload()
#         self.node_settings.reload()
#         last_log = self.project.logs[-1]
#
#         assert_equal(last_log.action, 'dropbox_node_authorized')
#         log_params = last_log.params
#         assert_equal(log_params['node'], self.project._primary_key)
#         assert_equal(last_log.user, self.user)
#
#     def test_dropbox_get_share_emails(self):
#         # project has some contributors
#         contrib = AuthUserFactory()
#         self.project.add_contributor(contrib, auth=Auth(self.user))
#         self.project.save()
#         url = api_url_for('dropbox_get_share_emails', pid=self.project._primary_key)
#         res = self.app.get(url, auth=self.user.auth)
#         result = res.json['result']
#         assert_equal(result['emails'], [u.username for u in self.project.contributors
#                                         if u != self.user])
#         assert_equal(result['url'], utils.get_share_folder_uri(self.node_settings.folder))
#
#     def test_dropbox_get_share_emails_returns_error_if_not_authorizer(self):
#         contrib = AuthUserFactory()
#         contrib.add_addon('dropbox')
#         contrib.save()
#         self.project.add_contributor(contrib, auth=Auth(self.user))
#         self.project.save()
#         url = api_url_for('dropbox_get_share_emails', pid=self.project._primary_key)
#         # Non-authorizing contributor sends request
#         res = self.app.get(url, auth=contrib.auth, expect_errors=True)
#         assert_equal(res.status_code, httplib.FORBIDDEN)
#
#     def test_dropbox_get_share_emails_requires_user_addon(self):
#         # Node doesn't have auth
#         self.node_settings.user_settings = None
#         self.node_settings.save()
#         url = api_url_for('dropbox_get_share_emails', pid=self.project._primary_key)
#         # Non-authorizing contributor sends request
#         res = self.app.get(url, auth=self.user.auth, expect_errors=True)
#         assert_equal(res.status_code, httplib.BAD_REQUEST)
