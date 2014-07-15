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


