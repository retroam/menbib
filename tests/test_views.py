# -*- coding: utf-8 -*-
from webtest_plus import TestApp
from nose.tools import *  # PEP8 asserts

from tests.base import OsfTestCase, URLLookup, assert_is_redirect
from tests.factories import AuthUserFactory
from website.util import api_url_for


from .utils import app, MenbibAddonTestCase

lookup = URLLookup(app)

class TestMenbibViews(OsfTestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.app.authenticate(*self.user.auth)

    def test_menbib_oauth_start(self):
        url = api_url_for('menbib_oauth_start_user')
        res = self.app.get(url)
        assert_is_redirect(res)

    def test_menbib_oauth_finish(self):
        url = api_url_for('menbib_oauth_finish')
        res = self.app.get(url)
        assert_is_redirect(res)
