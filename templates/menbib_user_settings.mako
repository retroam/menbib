## Template for the "Mendeley" section in the "Configure Add-ons" panel

<div id='menbibAddonScope' class='addon-settings scripted'>
    <h4 class='addon-title'>
        Mendeley
         <!-- <pre data-bind="text: ko.toJSON($data, null, 2)"></pre> -->
        <pre data-bind="text: ko.toJSON($data, null, 2)"></pre>
        <small class="authorized-by">
                 <!-- Delete Access Token Button -->

            <span data-bind="if: userHasAuth() && loaded()">
                authorized
                <span data-bind="if: menbibName()"> by {{ menbibName }} </span>
                <a data-bind="click: deleteKey" class="text-danger pull-right"
                   style="margin-top:4.8px">
                    Delete Access Token
                </a>
            </span>
                 <!-- Create Access Token Button -->
            <span data-bind="if: !userHasAuth() && loaded()">
                <a data-bind="attr: {href: urls().create}" class="text-primary pull-right"
                   style="margin-top:4.8px">
                    Create Access Token
                </a>
            </span>
        </small>
    </h4>

    <!-- Flashed Messages -->
    <div class="help-block">
        <p data-bind="html: message, attr: {class: messageClass}"></p>
    </div>
 </div>

<script>
    $script(['/static/addons/menbib/menbibUserConfig.js'], function() {
        // Endpoint for menbib user settings
        var url = '/api/v1/settings/menbib/';
        // Start up the MendeleyBibliography Config manager
        var menbib = new MenbibUserConfig('#menbibAddonScope', url);
    });
</script>

<%include file="profile/addon_permissions.mako" />