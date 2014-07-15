# -*- coding: utf-8 -*-
"""Persistence layer for the menbib addon.
"""


from website.addons.base import AddonUserSettingsBase, AddonNodeSettingsBase
from framework.auth import Auth
from framework import fields


class AddonMenbibUserSettings(AddonUserSettingsBase):
    """Stores user-specific information, including the Oauth access
    token.
    """
    access_token = fields.StringField(required=False)
    refresh_token = fields.StringField(required=False)
    token_type = fields.StringField(required=False)
    expires_in = fields.StringField(required=False)
    menbib_info = fields.StringField(required=False)


    @property
    def has_auth(self):
        return bool(self.access_token)

    def to_json(self, user=None):
        output = super(AddonMenbibUserSettings, self).to_json(self.owner)
        output['has_auth'] = self.has_auth
        return output

    def delete(self, save=True):
        self.clear()
        super(AddonMenbibUserSettings, self).delete(save)

    def clear(self):
        self.access_token = None
        for node_settings in self.addonmenbibnodesettings__authorized:
            node_settings.deauthorize(Auth(self.owner))
            node_settings.save()
        return self


class AddonMenbibNodeSettings(AddonNodeSettingsBase):

    user_settings = fields.ForeignField(
        'addonmenbibusersettings', backref='authorized'
    )
    folder = fields.StringField(default=None)

    @property
    def has_auth(self):
        """Whether an access token is associated with this node."""
        return bool(self.user_settings and self.user_settings.has_auth)

    def set_user_auth(self, user_settings):
        node = self.owner
        self.user_settings = user_settings
        node.add_log(
            action='menbib_node_authorized',
            auth=Auth(user_settings.owner),
            params={
                'project': node.parent_id,
                'node': node._primary_key,
            }
        )

    def set_folder(self, folder, auth):
        node = self.owner
        self.folder = folder
        node.add_log(
            action='menbib_folder_selected',
            save=True,
            params={
                'project': node.parent_id,
                'node': node._id,
                'folder': folder,
            },
            auth=auth,
        )

    def delete(self, save=True):
        self.deauthorize(add_log=False)
        super(AddonMenbibNodeSettings, self).delete(save)

    def deauthorize(self, auth=None, add_log=True):
        """Remove user authorization from this node and log the event."""

        node = self.owner
        folder = self.folder
        self.user_settings = None
        self.folder = None
        if add_log:
            self.owner.add_log(
                action='menbib_node_deauthorized',
                params={
                    'project': node.parent_id,
                    'node': node._id,
                    'folder': folder
                },
                auth=auth,
            )

    ##### Callback overrides #####

    def before_register_message(self, node, user):
        """Return warning text to display if user auth will be copied to a
        registration.
        """
        category, title = node.project_or_component, node.title
        if self.user_settings and self.user_settings.has_auth:
            # TODO:
            pass

    # backwards compatibility
    before_register = before_register_message

    def before_fork_message(self, node, user):
        """Return warning text to display if user auth will be copied to a
        fork.
        """
        category = node.project_or_component
        if self.user_settings and self.user_settings.owner == user:
            return ('Because you have authorized the Mendely add-on for this {category},'
                    'forking it will not transfer authentication to {category}').format(category=category)

    # backwards compatibility
    before_fork = before_fork_message

    def before_remove_contributor_message(self, node, removed):
        """Return warning text to display if removed contributor is the user
        who authorized the Mendeley addon
        """
        if self.user_settings and self.user_settings.owner == removed:
            category = node.project_or_component
            name = removed.fullname
            return ('The Mendeley add-on for this {category} is authenticated by {name}. '
                    'Removing this user will also remove write access to Mendeley '
                    'unless another contributor re-authenticates the add-on.'
                    ).format(**locals())

    # backwards compatibility
    before_remove_contributor = before_remove_contributor_message

    def after_register(self, node, registration, user, save=True):
        """After registering a node, copy the user settings and save the
        chosen folder.

        :return: A tuple of the form (cloned_settings, message)
        """
        clone, message = super(AddonMenbibNodeSettings, self).after_register(
            node, registration, user, save=False
        )
        # Copy user_settings and add registration data
        if self.has_auth and self.folder is not None:
            clone.user_settings = self.user_settings
            clone.registration_data['folder'] = self.folder
        if save:
            clone.save()
        return clone, message

    def after_fork(self, node, fork, user, save=True):
        """After forking, copy user settings if the user is the one who authorized
        the addon.

        :return: A tuple of the form (cloned_settings, message)
        """
        clone, _ = super(AddonMenbibNodeSettings, self).after_fork(
            node=node, fork=fork, user=user, save=False
        )

        if self.user_settings and self.user_settings.owner == user:
            clone.user_settings = self.user_settings
            message = 'Mendeley authorization copied to fork.'
        else:
            message = ('Mendeley authorization not copied to fork. You may '
                        'authorize this fork on the <a href="{url}">Settings</a>'
                        'page.').format(
                        url=fork.web_url_for('node_setting'))
        if save:
            clone.save()
        return clone, message

    def after_remove_contributor(self, node, removed):
        """If the removed contributor was the user who authorized the Menbib
        addon, remove the auth credentials from this node.
        Return the message text that will be displayed to the user.
        """
        if self.user_settings and self.user_settings.owner == removed:
            self.user_settings = None
            self.save()
            name = removed.fullname
            url = node.web_url_for('node_setting')
            return ('Because the Mendeley add-on for this project was authenticated'
                    'by {name}, authentication information has been deleted. You '
                    'can re-authenticate on the <a href="{url}">Settings</a> page'
                    ).format(**locals())