define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'routers',
], function($, _, Backbone, Marionette, Routers) {

    'use strict';

    var oldSync = Backbone.sync;
    Backbone.sync = function(method, model, options){
        options.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', $("input[name='csrfmiddlewaretoken']").val());
        };
        return oldSync(method, model, options);
    };

    var TaggedApp = Marionette.Application.extend({
        initialize: function(options) {
            console.log('App initialized...', options);
        }
    });

    var taggedApp = new TaggedApp({ example: 'sample' });
    taggedApp.router = new Routers.MyRouter();

    taggedApp.on('start', function() {
        console.log('App start triggered...');
        Backbone.history.start({ pushState: true });
    });

    return taggedApp;
});
