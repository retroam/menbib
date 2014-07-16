from nose.tools import *  # PEP8 asserts
from website.addons.menbib.api import Mendeley

from tests.base import OsfTestCase
from tests.factories import UserFactory

from website.addons.base.exceptions import AddonError
from website.addons.menbib.model import AddonMenbibUserSettings
from website.addons.menbib.tests.factories import (
    MenbibNodeSettingsFactory,MenbibUserSettingsFactory)

from website.addons.menbib.client import (
    get_client, get_node_addon_client, get_node_client, get_client_from_user_settings
)

class TestCore(OsfTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.add_addon('menbib')
        self.user.save()

        self.settings = self.user.get_addon('menbib')
        self.settings.access_token = '12345'
        self.settings.refresh_token = 'abcde'
        self.settings.save()

    def test_get_addon_returns_menbib_user_settings(self):
        result = self.user.get_addon('menbib')
        assert_true(isinstance(result, AddonMenbibUserSettings))


class TestClientHelpers(OsfTestCase):
    def setUp(self):
        self.user_settings = MenbibUserSettingsFactory()
        self.node_settings = MenbibNodeSettingsFactory(user_settings=self.user_settings)
        self.user = self.user_settings.owner
        self.node = self.node_settings.owner

    def test_get_client_returns_a_menbib_client(self):
        client = get_client(self.user)
        assert_true(isinstance(client, Mendeley))

    def test_get_client_raises_addon_error_if_user_doesnt_have_addon_enabled(self):
        user_no_menbib = UserFactory()
        with assert_raises(AddonError):
            get_client(user_no_menbib)

    def test_get_node_addon_client(self):
        client = get_node_addon_client(self.node_settings)
        assert_true(isinstance(client, Mendeley))

    def test_get_node_client(self):
        client = get_node_client(self.node)
        assert_true(isinstance(client, Mendeley))

    def test_get_client_from_user_settings(self):
        client = get_client_from_user_settings(self.user_settings)
        assert_true(isinstance(client, Mendeley))