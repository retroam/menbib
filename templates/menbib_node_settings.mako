

<div id="menbibScope" class="scripted">
    <pre data-bind="text: ko.toJSON($data, null, 2)"></pre>
    <h4 class="addon-title">
        Mendeley
        <small class="authorized-by">
            <span data-bind="if: nodeHasAuth">
                authorized by <a data-bind="attr.href: urls().owner">{{ownerName}}</a>
                <a data-bind="click: deauthorize" style="margin-top: 4.8px"
                        class="text-danger pull-right">Deauthorize</a>
            </span>

            <!-- Import Access Token Button -->
            <span data-bind="if: showImport">
                <a data-bind="click: importAuth" href="#" class="text-primary pull-right">
                    Import Access Token
                </a>
            </span>

              <!-- Oauth Start Button -->
            <span data-bind="if: showTokenCreateButton">
                <a data-bind="attr.href: urls().auth" class="text-primary pull-right">
                    Create Access Token
                </a>
            </span>

        </small>
    </h4>


    <!-- Settings Pane -->
    <div class="menbib-settings" data-bind='if: showSettings'>
        <div class="row">
            <div class="col-md-12">
                <p><strong>Current Linked Folder:</strong></p>

                <!-- The linked folder -->
                <div class="selected-folder">
                    <i data-bind="visible: linked().name" class="icon-folder-close-alt"></i>
                    <a data-bind="attr.href: urls().files" class="selected-folder-name">
                        {{folderName}}
                    </a>

                    <p data-bind="if: linked().id === null" class="text-muted">No content linked</p>
                </div>

                <!-- Folder buttons -->
                <div class="btn-group">
                    <button data-bind="click: togglePicker,
                                        css: {active: currentDisplay() === PICKER}"
                            class="btn btn-sm btn-menbib"><i class="icon-edit"></i> Change</button>
                </div>


                <!-- Folder picker -->
                <div class="menbib-widget">
                    <p class="text-muted text-center menbib-loading-text" data-bind="visible: loading">
                    Loading folders...</p>

                    <div data-bind="if: currentDisplay() === PICKER">
                        <div id="menbibGrid"
                             class="filebrowser hgrid menbib-folder-picker"></div>
                    </div>

                    <!-- Queued selection -->
                    <div class="menbib-confirm-selection"
                        data-bind="visible: currentDisplay() === PICKER && selected()">
                        <form data-bind="submit: submitSettings">

                            <h4 data-bind="if: selected" class="menbib-confirm-dlg">
                                Connect Mendeley {{selectedFolderType}} &ldquo;{{ selectedFolderName }}&rdquo;?
                            </h4>
                            <div class="pull-right">
                                <button class="btn btn-default"
                                        data-bind="click: cancelSelection">
                                    Cancel
                                </button>
                                <input type="submit"
                                       class="btn btn-primary"
                                       value="Submit" />
                            </div>
                        </form>
                    </div><!-- end .menbib-confirm-selection -->

                </div>
            </div><!-- end col -->
        </div><!-- end row -->
    </div><!-- end .menbib-settings -->

    <!-- Flashed Messages -->
    <div class="help-block">
        <p data-bind="html: message, attr.class: messageClass"></p>
    </div>


</div>

<script>
    $script(['/static/addons/menbib/menbibNodeConfig.js']);
    $script.ready('menbibNodeConfig', function() {
        var url = '${node["api_url"] + "menbib/config/"}';
        var menbib = new MenbibNodeConfig('#menbibScope',url, '#menbibGrid');
    });
</script>