""" Factory boy factories for the Mendeley addon."""

from factory import SubFactory, Sequence
from tests.factories import ModularOdmFactory, UserFactory, ProjectFactory

from website.addons.menbib.model import (
    AddonMenbibUserSettings, AddonMenbibNodeSettings
)


class MenbibUserSettingsFactory(ModularOdmFactory):
    FACTORY_FOR = AddonMenbibUserSettings

    owner = SubFactory(UserFactory)
    oauth_access_token = Sequence(lambda n: 'abcdef{0}'.format(n))


class MenbibNodeSettingsFactory(ModularOdmFactory):
    FACTORY_FOR = AddonMenbibNodeSettings

    owner = SubFactory(ProjectFactory)
    user_settings = SubFactory(MenbibUserSettingsFactory)
    folder = 'COS papers'

