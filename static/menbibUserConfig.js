/**
 * Module that controls the MendeleyBibliography user settings. Includes Knockout view-model
 * for syncing data.
 */
;(function (global, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['knockout', 'jquery', 'osfutils', 'knockoutpunches', 'language'], factory);
    } else {
        global.MenbibUserConfig  = factory(ko, jQuery);
    }
}(this, function(ko, $) {
    // Enable knockout punches
    ko.punches.enableAll();

    var language = $.osf.Language.Addons.mendeley;

    function ViewModel(url) {
        var self = this;
        self.userHasAuth = ko.observable(false);
        self.menbibName = ko.observable();
        self.urls = ko.observable({});
        self.loaded = ko.observable(false);
        $.ajax({
            url: url, type: 'GET', dataType: 'json',
            success: function(response){
                var data = response.result;
                self.userHasAuth(data.userHasAuth);
                self.menbibName(data.menbibName);
                self.urls(data.urls);
                self.loaded(true);
            },
            error: function(xhr, textStatus, error){
                console.error(textStatus); console.error(error);
                self.changeMessage('Could not retrieve settings. Please refresh the page or ' +
                   'contact <a href="mailto: support@cos.io">support@cos.io</a> if the ' +
                   'problem persists.', 'text-warning');

            }
        });
        // Flashed messages
        self.message = ko.observable('');
        self.messageClass = ko.observable('text-info');

        function sendDeauth(){
            return $.ajax({
                url: self.urls().delete,
                type: 'DELETE',
                success: function() {
                    location.reload()
                },
                error: function(){
                    self.changeMessage(language.deauthError, 'text-danger');
                }

            });
        }

        self.deleteKey = function() {
            bootbox.confirm({
                title: "Delete Mendeley Token?",
                message: language.confirmDeauth,
                callback: function(confirmed){
                    if (confirmed) {
                        sendDeauth();
                    }
                }
            })
        }
    };

    function MenbibUserConfig(selector, url) {
        // Initialization code
        var self = this;
        self.selector = selector;
        self.url = url;
        // On success, instantiate and bind the ViewModel
        self.viewModel = new ViewModel(url);
        $.osf.applyBindings(self.viewModel, '#menbibAddonScope');
    }
    return MenbibUserConfig

}));