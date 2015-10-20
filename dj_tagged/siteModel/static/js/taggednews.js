define([
    'jquery',
    'underscore',
    'backbone',
    'routers',
], function($, _, Backbone, Routers) {

    'use strict';
    
    (function($){
        var oldSync = Backbone.sync;
        Backbone.sync = function(method, model, options){
            options.beforeSend = function(xhr){
                xhr.setRequestHeader('X-CSRFToken', $("input[name='csrfmiddlewaretoken']").val());
            };
            return oldSync(method, model, options);
        };
        
        window.App = {
            Router: {}
        };

        App.router = new Routers.WorkspaceRouter();

        Backbone.history.start({ pushState: true });

    })(jQuery);
});
