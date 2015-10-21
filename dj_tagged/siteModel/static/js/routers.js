define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'views',
], function($, _, Backbone, Marionette, Views) {

    'use strict';

    var MyRouter = Marionette.AppRouter.extend({
        appRoutes: {

        },

        routes: {
            "": "home",
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
        'MyRouter': MyRouter
    };
});
