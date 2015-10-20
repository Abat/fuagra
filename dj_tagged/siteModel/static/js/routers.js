define([
    'jquery',
    'underscore',
    'backbone',
    'views',
], function($, _, Backbone, Views) {

    'use strict';

    var WorkspaceRouter = Backbone.Router.extend({

        routes: {
            "": "home",
            "about": "about",   // #about
            "comments": "comments"
        },

        home: function() {
            console.log("home route triggered");
            var newsView = new Views.NewsView();
        },

        comments: function() {
            console.log("comments route triggered");
            //var newsView = new Views.NewsView();
        }
    });


    return {
        'WorkspaceRouter': WorkspaceRouter
    };
});
