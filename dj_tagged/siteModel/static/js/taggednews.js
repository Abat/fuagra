define([
    'jquery',
    'underscore',
    'backbone',
    'views',
], function($, _, Backbone, Views) {

    'use strict';
    
    (function($){
        var oldSync = Backbone.sync;
        Backbone.sync = function(method, model, options){
            options.beforeSend = function(xhr){
                xhr.setRequestHeader('X-CSRFToken', $("input[name='csrfmiddlewaretoken']").val());
            };
            return oldSync(method, model, options);
        };
        var newsView = new Views.NewsView();
    })(jQuery);
});
