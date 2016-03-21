define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'polyglot',
    'routers',
    'views',
    'text!templates/layout.html',
], function($, _, Backbone, Marionette, Collections, Polyglot, Routers, Views, layoutT) {

    var taggedApp;

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

    taggedApp = new TaggedApp({ example: 'sample' });

    var RootLayout = Marionette.LayoutView.extend({
        el: '.layout',
        template: _.template(layoutT),

        regions: {
            special_top: '#special_top',
            content: '#content',
            side: '#side'
        }
    });
    taggedApp.rootLayout = new RootLayout();
    taggedApp.rootLayout.render();

    taggedApp.router = new Routers.MyRouter();

    taggedApp.on('start', function(phrases) {
        console.log('App start triggered...');
        var locale = localStorage.getItem('locale')
        self.polyglot = new Polyglot({ phrases: phrases, locale: locale });
        Backbone.history.start({ pushState: true });
    });    

    taggedApp.news = new Collections.NewsListCollection();

    return taggedApp;
});
